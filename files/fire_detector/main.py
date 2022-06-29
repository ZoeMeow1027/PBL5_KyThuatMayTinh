
import threading
import numpy as np
from PIL import Image
import cv2
import json

import files.fire_detector.detected as fire_detector_detected
import files.utils as fire_utils

interpreter = None
input_details = None
output_details = None

room_status = None

is_running = False
count_max_alert = 5
count_current_alert = 0

DATETIME_AFTERNOTIFIED_MAIN = 0

def FireDetect(frame, pi_mode):
    global interpreter
    global input_details
    global output_details
    global count_max_alert
    global count_current_alert
    global room_status

    global is_running
    if (is_running):
        return
    is_running = True

    if (pi_mode):
        if (DATETIME_CURRENT - DATETIME_AFTERNOTIFIED_MAIN > 60):
            fire_detector_physcal.ToggleBuzzer(False)

    CAMERA_DETECT = False
    PHYSCAL_DETECT = False

    frame2 = frame

    new_img = cv2.resize(frame2, (224, 224))
    new_img = new_img.astype(np.float32)
    new_img /= 255.

    # input_details[0]['index'] = the index which accepts the input
    interpreter.set_tensor(input_details[0]['index'], [new_img])

    # realizar la prediccion del interprete
    interpreter.invoke()

    # output_details[0]['index'] = the index which provides the input
    output_data = interpreter.get_tensor(output_details[0]['index'])

    print("The output is {}".format(output_data))
    # im = Image.fromarray(frame, 'RGB')
    # im.resize((224, 224))
    # img_array = tf.keras.preprocessing.image.img_to_array(im)
    # img_array = np.expand_dims(img_array, axis=0) / 255
    # probabilities = interpreter.predict(img_array)[0]
    # #Calling the predict method on model to predict 'fire' on the image
    prediction = np.argmax(output_data[0])
    #if prediction is 0, which means there is fire in the frame.
    if prediction == 0: 
        # Convert frame to Gray
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        print(output_data[prediction])

        # TODO: Check for physcal here before upload to server!
        print('I: Fire detected! Checking physcal device...')
        CAMERA_DETECT = True

    if (room_status != None):
        print(json.dumps(room_status))
        if (room_status['temperature'] >= 35 and
            room_status['co_detected'] == True and
            (room_status['flame_detected'] == True or CAMERA_DETECT == True)
            ):
            PHYSCAL_DETECT = True

    # This line is only for debugging. Do not add to release code.
    PHYSCAL_DETECT = CAMERA_DETECT

    if (PHYSCAL_DETECT):
        # TODO: Send to Firebase here!
        # This function needs to be ran with new thread (to release
        # this process for continue detecting another frame)
        fire_detector_detected.fire_detected(frame, room_status)

        if (pi_mode):
            DATETIME_CURRENT = fire_utils.get_current_date_unix()
            if (DATETIME_CURRENT - DATETIME_AFTERNOTIFIED_MAIN > 60):
                import files.fire_detector.physcal_real as fire_detector_physcal
                fire_detector_physcal.ToggleBuzzer(True)
                DATETIME_AFTERNOTIFIED_MAIN = DATETIME_CURRENT
    
    is_running = False

attempt_physcal_current = 1
attempt_physcal_max = 10
def __fire_detector_physcal__(pi_mode: bool = False):
    global attempt_physcal_current
    global attempt_physcal_max
    global room_status
    while True:
        try:
            if (pi_mode):
                import files.fire_detector.physcal_real as fire_detector_physcal
                room_status = fire_detector_physcal.FireDetect_Physcal()
            else:
                import files.fire_detector.physcal_demo as fire_detecter_demo
                room_status = fire_detecter_demo.FireDetect_Demo()
            attempt_physcal_current = 1
        except Exception as ex:
            print('W: Can\'t get physcal information. Attempted {}/{}. Retrying...'.format(
                attempt_physcal_current,
                attempt_physcal_max
            ))
            attempt_physcal_current += 1
            if attempt_physcal_current > attempt_physcal_max:
                raise Exception("E: Can't get physcal information. Too many attempts. Try again.\nMessage: {}".format(ex))

def fire_detector_init(
    camera_fps: int = 15,
    pi_mode: bool = False
):
    MODAL_PATH = 'data/modal/detect.tflite'

    global interpreter
    global input_details
    global output_details

    print('I: Initializing tensorflow-lite modal...')
    if pi_mode:
        # For tensorflow-lite
        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path=MODAL_PATH)
    else:
        # For full tensorflow
        import tensorflow as tf
        interpreter = tf.lite.Interpreter(model_path=MODAL_PATH)

    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    # print(input_details)
    # print(output_details)

    # Init video capture
    # Detect your camera in cv2.VideoCapture(x)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, camera_fps)
    fps = int(cap.get(5))
    print("I: FPS set in settings (video only):", fps)

    if (cap.isOpened() == False):
        raise Exception('E: Your camera is used by another process!\nClose all programs use this camera and try again.')
    
    thread_physcal = threading.Thread(target=__fire_detector_physcal__, args=(pi_mode, ))
    thread_physcal.start()

    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        thread_detect = threading.Thread(target=FireDetect, args=(frame, pi_mode, ))
        thread_detect.start()
        # FireDetect(interpreter, input_details, output_details, frame)
        
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release camera and close all windows.
    cap.release()
    cv2.destroyAllWindows()
    pass


import threading
import numpy as np
import cv2
import json

import files.fire_detector.detected as fire_detector_detected
import files.utils as firebase_utils

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
    global DATETIME_AFTERNOTIFIED_MAIN

    global is_running
    if (is_running):
        return
    is_running = True

    DATETIME_CURRENT = firebase_utils.get_current_date_unix()

    if (pi_mode):
        if (DATETIME_CURRENT - DATETIME_AFTERNOTIFIED_MAIN > 60000):
            import files.fire_detector.physcal_real as fire_detector_physcal
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

    print("{time} I: The output is {out}".format(
        out=output_data,
        time=firebase_utils.get_current_date()
    ))
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
        print('{time} I: Fire detected! Checking physcal device...'.format(
            time=firebase_utils.get_current_date()
        ))
        CAMERA_DETECT = True

    if (room_status != None):
        if (room_status['temperature'] != None and room_status['humidity'] != None):
            if (
                room_status['co_detected'] == True and
                room_status['flame_detected'] == True
            ):
                PHYSCAL_DETECT = True
        else:
            import files.fire_detector.physcal_demo as fire_detector_demo
            room_status['temperature'] = fire_detector_demo.FireDetect_Demo()['temperature']
            room_status['humidity'] = fire_detector_demo.FireDetect_Demo()['humidity']       

    # This line is only for debugging. Do not add to release code.
    # PHYSCAL_DETECT = CAMERA_DETECT

    if (PHYSCAL_DETECT and CAMERA_DETECT):
        # TODO: Send to Firebase here!
        # This function needs to be ran with new thread (to release
        # this process for continue detecting another frame)
        fire_detector_detected.fire_detected(frame, room_status)

        if (pi_mode):
            if (DATETIME_CURRENT - DATETIME_AFTERNOTIFIED_MAIN > 60000):
                import files.fire_detector.physcal_real as fire_detector_physcal
                fire_detector_physcal.ToggleBuzzer(True)
                DATETIME_AFTERNOTIFIED_MAIN = DATETIME_CURRENT
    
    is_running = False

def __fire_detector_physcal__(pi_mode: bool = False):
    global room_status
    while True:
        if (pi_mode):
            import files.fire_detector.physcal_real as fire_detector_physcal
            ATTEMPT_TRIED = 0
            while (ATTEMPT_TRIED < 15):
                try:
                    room_status = fire_detector_physcal.FireDetect_Physcal()
                except:
                    ATTEMPT_TRIED += 1
            if (ATTEMPT_TRIED >= 15):
                import files.fire_detector.physcal_demo as fire_detecter_demo
                room_status = fire_detecter_demo.FireDetect_Demo()
        else:
            import files.fire_detector.physcal_demo as fire_detecter_demo
            room_status = fire_detecter_demo.FireDetect_Demo()

def fire_detector_init(
    camera_fps: int = 15,
    pi_mode: bool = False
):
    MODAL_PATH = 'data/modal/detect.tflite'

    global interpreter
    global input_details
    global output_details

    print('{time} I: Initializing tensorflow-lite modal...'.format(time=firebase_utils.get_current_date()))
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
    print("{time} I: FPS set in settings (video only): {fps}".format(
            time=firebase_utils.get_current_date(),
            fps=fps
        ))

    if (cap.isOpened() == False):
        raise Exception('{time} E: Your camera is used by another process!\nClose all programs use this camera and try again.'.format(time=firebase_utils.get_current_date()))
    
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        thread_physcal = threading.Thread(target=__fire_detector_physcal__, args=(pi_mode, ))
        thread_physcal.start()

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

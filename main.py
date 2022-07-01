
from files.auth.init_firebase_auth import *
from files.auth.init_firebase_uid import *
from files.init_modal import *
from files.init_settings import *
from files.utils import *

import files.fire_detector.main as fire_detector_process
import files.auth.firebase_fcm as firebase_cloud_messaging
import files.utils as firebase_utils

create_data_folder()

# Load settings, or create new settings if not exist
DEVICE_SETTINGS = init_settings()
    
try:
    # Authenticate firebase
    init_firebase_auth()

    # Check if device is registered in firebase
    try:
        if (init_firebase_uid_check(DEVICE_SETTINGS['firebase_uid']) == False):
            raise Exception('{time} E: Device UID isn\'t exist!\nMay be you aren\'t registered this device?\nRegister device with UID: {uid}'
                .format(time=firebase_utils.get_current_date(), uid=DEVICE_SETTINGS['firebase_uid'])
            )
        else:
            print('{time} I: Your deivce is in our firebase.'.format(time=firebase_utils.get_current_date()))
    except Exception as ex:
        # print(ex)
        # If not exist uid in server, execute here!
        raise ex

    # Download modal or skip if up-to-date.
    init_modal()

    # Register device token
    for st in DEVICE_SETTINGS['phone_token']:
        firebase_cloud_messaging.subscribe_news(st)

    # Initialize physcal device
    if (DEVICE_SETTINGS['pi_mode']):
        import files.fire_detector.physcal_real as fire_detector_physcal
        fire_detector_physcal.FireDetect_Setup()

    # Init main project: Fire detector
    fire_detector_process.fire_detector_init(
        DEVICE_SETTINGS['camera_fps'],
        pi_mode=DEVICE_SETTINGS['pi_mode']
    )
except Exception as ex:
    print('{time} E: A critical error has occurred and this program must be stopped. Message: {ex}'.format(time=firebase_utils.get_current_date(), ex=ex))
finally:
    if (DEVICE_SETTINGS['pi_mode']):
        import files.fire_detector.physcal_real as fire_detector_physcal
        fire_detector_physcal.FireDetect_Release()
        fire_detector_physcal.ToggleBuzzer(False)

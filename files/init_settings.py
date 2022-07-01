import json
import os

import files.utils as firebase_utils


__SETTINGS_PATH__ = 'data/settings.json'
__FIREBASE_CONFIG_PATH__ = 'auth/firebase_configs.json'

def init_settings_save(settings: dict):
    open(__SETTINGS_PATH__, 'w').write(json.dumps(settings))
    return

def init_settings_createnew() -> dict:
    SETTINGS_INIT = {
        'firebase_uid': firebase_utils.generate_uuid(),
        'camera_fps': 15,
        'phone_token': [],
        'pi_mode': True
    }
    init_settings_save(SETTINGS_INIT)
    return SETTINGS_INIT

def init_settings() -> dict:
    if (os.path.isfile(__SETTINGS_PATH__) == False):
        return init_settings_createnew()
    else:
        return json.loads(open(__SETTINGS_PATH__, 'r').read())

def init_firebase_config_createnew() -> dict:
    FIREBASE_INIT = {
        "databaseURL": "https://nhom-pbl5-default-rtdb.firebaseio.com",
        "storageBucket": "nhom-pbl5.appspot.com"
    }
    print('{time} W: No config found for firebase! Creating one...'.format(time=firebase_utils.get_current_date()))
    print('{time} W: You need to edit config in {config} for take effect!'.format(time=firebase_utils.get_current_date(), config=__FIREBASE_CONFIG_PATH__))
    open(__FIREBASE_CONFIG_PATH__, 'w').write(json.dumps(FIREBASE_INIT))
    return FIREBASE_INIT

def init_firebase_configs() -> dict:
    if (os.path.isfile(__FIREBASE_CONFIG_PATH__) == False):
        return init_firebase_config_createnew()
    else:
        return json.loads(open(__FIREBASE_CONFIG_PATH__, 'r').read())

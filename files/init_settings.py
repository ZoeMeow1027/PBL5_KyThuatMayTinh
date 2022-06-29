import json
import os

from files.utils import *

__SETTINGS_PATH__ = 'data/settings.json'

def init_settings_save(settings: dict):
    open(__SETTINGS_PATH__, 'w').write(json.dumps(settings))
    return

def init_settings_createnew() -> dict:
    SETTINGS_INIT = {
        'firebase_uid': generate_uuid(),
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

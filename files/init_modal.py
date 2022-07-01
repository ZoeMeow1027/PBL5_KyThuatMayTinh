from firebase_admin import db
import os
import requests

import files.utils as firebase_utils

__MODAL_PATH__ = "data/modal.zip"
__MODAL_VERSION_PATH__ = "data/modal.version"

def init_modal_exist() -> bool:
    return os.path.isfile(__MODAL_PATH__) and os.path.isfile(__MODAL_VERSION_PATH__)

def init_modal_version_compare(old_ver: str, new_ver: str) -> bool:
    """
    Returns:
        True if new_ver is larger than old_ver. Otherwise False.
    """
    old_ver_arr = old_ver.split('.')
    new_ver_arr = new_ver.split('.')
    max = len(old_ver_arr) if len(old_ver_arr) < len(new_ver_arr) else len(new_ver_arr)
    result = False
    for i in range(0, max, 1):
        if int(new_ver_arr[i]) > int(old_ver_arr[i]):
            result = True
            break
    return result

def init_modal(force_update: bool = False, auto_update: bool = True):
    print('{time} I: Checking for updates...'.format(
        time=firebase_utils.get_current_date()
    ))
    ref = db.reference('/files/modal/')
    # Get information about current modal.
    modal_info = ref.get()
    print('{time} I: Server modal version: {ver}'.format(
        time=firebase_utils.get_current_date(),
        ver=modal_info['version']
    ))

    need_update = False
    if (init_modal_exist() == False):
        need_update = True
    else:
        current_ver = open(__MODAL_VERSION_PATH__, 'r').read()
        print('{time} I: Current modal version: {ver}'.format(
            time=firebase_utils.get_current_date(),
            ver=current_ver
        ))
        if (init_modal_version_compare(current_ver, modal_info['version'])):
            need_update = True

    if (force_update):
        print('{time} I: Force update enabled.'.format(time=firebase_utils.get_current_date()))
        need_update = True
    
    if (need_update and auto_update):
        print('{time} I: Downloading modal...'.format(time=firebase_utils.get_current_date()))
        # Download modal
        response = requests.get(modal_info['dl'])
        if response.status_code != 200:
            raise Exception('{time} E: Download modal failed!'.format(time=firebase_utils.get_current_date()))
        # File name and full path
        # Write modal to file
        f = open(__MODAL_PATH__, 'wb')
        f.write(response.content)
        f.close()
        print('{time} I: Checking MD5 for modal...'.format(time=firebase_utils.get_current_date()))
        # Check md5
        if modal_info['md5'] != firebase_utils.chech_md5_from_file(__MODAL_PATH__):
            raise Exception('{time} E: MD5 mismatch!'.format(time=firebase_utils.get_current_date()))
        # Write version to file
        f = open(__MODAL_VERSION_PATH__, 'w')
        f.write(modal_info['version'])
        f.close()
        # Extract file
        print('{time} I: Extracting modal file...'.format(time=firebase_utils.get_current_date()))
        firebase_utils.extract_zip(__MODAL_PATH__, 'data/modal')
        print('{time} I: Completed downloading model!'.format(time=firebase_utils.get_current_date()))
    elif auto_update == False:
        Exception('{time} E: Modal are out of date!'.format(time=firebase_utils.get_current_date()))
    else:
        print('{time} I: Your current model are up-to-date.'.format(time=firebase_utils.get_current_date()))

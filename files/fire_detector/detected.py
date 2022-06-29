import os
from firebase_admin import storage
from PIL import Image
import json

import files.init_settings as fire_init_settings
import files.utils as fire_utils
import files.auth.init_firebase_uid as firebase_auth_uid
import files.auth.firebase_fcm as firebase_cloud_messaging

DATETIME_AFTERNOTIFIED = 0

def fire_detected(frame, physcal_info):
    global DATETIME_AFTERNOTIFIED
    try:
        if (os.path.isdir('data/image_log') == False):
            os.mkdir('data/image_log/')
        DEVICE_UID = fire_init_settings.init_settings()['firebase_uid']
        DATE_UNIQUE = fire_utils.get_current_date_unix()
        FILE_NAME = 'fire_{uid}_{date}.jpg'.format(
            uid=DEVICE_UID,
            date=DATE_UNIQUE
        )
        FILE_PATH = '{folder_path}/{file_path}'.format(
            folder_path='data/image_log',
            file_path=FILE_NAME
        )

        # Save frame before uploading to firebase
        print('I: Saving detected fire frame to file...')
        image_pillow = Image.fromarray(frame)
        image_pillow.save(FILE_PATH)

        # Upload to firebase here!
        print('I: Uploading to firebase storage...')
        bucket = storage.bucket()
        blob = bucket.blob('fire_image/' + FILE_NAME)
        blob.upload_from_filename(FILE_PATH)
        blob.make_public()

        # Get blob public url and save to realtime database
        print('I: Writing to firebase (realtime database)...')
        firebase_auth_uid.init_firebase_uid_addnotify(DEVICE_UID, DATE_UNIQUE, blob.public_url, physcal_info)

        data = {
            "date": str(DATE_UNIQUE),
            "image_url": blob.public_url,
            "physcal_info": json.dumps(physcal_info)
        }
        CURRENT_DATETIME_UNIX = fire_utils.get_current_date_unix()
        if (CURRENT_DATETIME_UNIX - DATETIME_AFTERNOTIFIED > (60 * 1000)):
            print('I: Sending to device...')
            firebase_cloud_messaging.send_topic_push(
                title = "Có cháy xảy ra tại nơi thiết bị bạn đã đặt!",
                body = "Mau đến kiểm tra hiện trường!",
                data = data
            )
            DATETIME_AFTERNOTIFIED = CURRENT_DATETIME_UNIX
        else:
            print('I: Not send to phone (wait for {}s for more)...'.format(
                60 - (CURRENT_DATETIME_UNIX - DATETIME_AFTERNOTIFIED)
            ))

        print('I: Completed writing to firebase! Date: {date}'.format(date=DATE_UNIQUE))
    except Exception as ex:
        print('W: Failed while writing to firebase! Message: {ex}'.format(ex=ex))
    pass

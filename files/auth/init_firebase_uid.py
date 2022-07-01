from firebase_admin import db
import files.utils as file_utils

def init_firebase_uid_check(uid: str) -> bool:
    ref = db.reference('/devices/')
    modal_info = ref.get()
    if modal_info == None:
        return False
    found_ = filter(lambda item: item['token'] == uid, modal_info)
    if (len(list(found_)) > 0):
        return True
    else:
        return False

def init_firebase_uid_addnotify(uid: str, date, url: str, physcal_info: dict) -> bool:
    try:
        ref = db.reference('/devices/')
        modal_info = ref.get()
        for i in range (0, len(modal_info)):
            if (modal_info[i]['token'] == uid):
                if ('notifications' not in modal_info[i].keys()):
                    modal_info[i]['notifications'] = []
                modal_info[i]['notifications'].append(
                    {
                        'date': date,
                        'image_url': url,
                        'physcal_info': physcal_info
                    }
                )
            ref.set(modal_info)
            return True
        raise Exception('{time} E: Device was not registered!'.format(time=file_utils.get_current_date()))
    except Exception as ex:
        print('{time} W: Write to firebase failed! Message: {ex}'.format(ex=ex, time=file_utils.get_current_date()))
        return False

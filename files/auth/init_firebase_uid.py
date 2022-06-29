from firebase_admin import db

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

def init_firebase_uid_addnotify(uid: str, date, url: str) -> bool:
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
                    }
                )
            ref.set(modal_info)
            return True
        raise Exception('Device was not registered!')
    except Exception as ex:
        print('W: Write to firebase failed! Message: {ex}'.format(ex=ex))
        return False

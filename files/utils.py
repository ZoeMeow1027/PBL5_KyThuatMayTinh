from datetime import datetime
import os
import hashlib
import uuid
import time
import zipfile

def create_data_folder():
    try:
        if (os.path.isdir('data') == False):
            os.makedirs('data')
        return
    except Exception as ex:
        print('{time} E: Failed while creating data folder! Message: {ex}'.format(ex=ex, time=get_current_date()))
        raise ex

def extract_zip(file_path: str, folder_path: str):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(folder_path)

def chech_md5_from_file(path: str) -> str:
    return hashlib.md5(open(path,'rb').read()).hexdigest()

def get_current_date() -> str:
    return datetime.now()

def generate_uuid() -> str:
    return str(uuid.uuid4())

def get_current_date_unix() -> int:
    return int(time.time() * 1000)

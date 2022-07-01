import firebase_admin
from firebase_admin import credentials, initialize_app

import files.init_settings as firebase_settings
import files.utils as firebase_utils

__FIREBASE_PRIVATE_KEY__ = 'auth/google-services.json'

def init_firebase_auth():
    print('{time} I: Authenticating firebase...'.format(firebase_utils.get_current_date()))
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate(__FIREBASE_PRIVATE_KEY__)
    # Load firebase configs
    firebase_configs = firebase_settings.init_firebase_configs()
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, firebase_configs)

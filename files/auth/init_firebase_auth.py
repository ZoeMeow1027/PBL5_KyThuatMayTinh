import firebase_admin
from firebase_admin import credentials, initialize_app

def init_firebase_auth():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('files/auth/nhom-pbl5-firebase-adminsdk-nezel-7a450a771d.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://nhom-pbl5-default-rtdb.firebaseio.com",
        'storageBucket': 'nhom-pbl5.appspot.com'
    })

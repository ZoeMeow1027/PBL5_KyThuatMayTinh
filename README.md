# PBL5_KyThuatMayTinh
Project-based Learning 5 for Computer Engineering. Fire detector using Machine Learning, Android, Firebase and Raspberry Pi.

# What's going on?
- You need to initiatize Firebase first. To complete this:
  - Create a folder named `auth`
  - In folder `auth`, create a file named `firebase_configs.json` and confis follow this data:
```json
{
    "databaseURL": "YOUR_REALTIME_DATABASE_URL",
    "storageBucket": "YOUR_STORAGE_URL (make sure not gs:// in string)"
}
```
    - Note: If you run this project now, this will also be created, but you still need config your `firebase_configs.json` file.
  - Create a Firebase Service Account key. To do this, go to your Firebase project. Then go to Project Settings -> Service accounts -> Firebase Admin SDK. Create a new here!
  - After these step, a json file contains private key will be downloaded. Rename to `google-services.json` and move to project `auth` folder.
  - You are done!

# Wanna to run on full Tensorflow?
- Edit 'pi_mode' to false in data/settings.json.
- Note this will be disable all physcal components (will run on physcal_demo instead of physcal_real).

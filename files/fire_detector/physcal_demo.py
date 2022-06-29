import time

def FireDetect_Demo():
    result = {}
    result['datetime_unix'] = int(time.time())
    result['temperature'] = 35
    result['humidity'] = 60
    result['co_detected'] = True
    result['flame_detected'] = False
    return result

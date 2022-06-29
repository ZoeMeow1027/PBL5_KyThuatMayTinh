
import os
import time

TIME_DELAY_RELAUNCH = 10

while (True):
    exit_code = os.system('python3 main.py')
    print('Current process has exited with code {code}.\nRe-launching after {time_relaunch} second(s)...'
        .format(code=exit_code, time_relaunch=TIME_DELAY_RELAUNCH)
    )
    time.sleep(TIME_DELAY_RELAUNCH)


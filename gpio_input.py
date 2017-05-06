#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

''' func: wait_for_trigger()
    if the status fit the expect status return True,
    else waitting ... (forever -_^) '''
def wait_for_trigger(gpio, expect_status):
    STATUS = {'rising': GPIO.RISING, 'falling': GPIO.FALLING, 'both': GPIO.BOTH}

    for channel in gpio:
        GPIO.add_event_detect(channel, STATUS[expect_status])

    jump = False
    while True:
        for channel in gpio:
            if GPIO.event_detected(channel):
                jump = True
                break

        if jump:
            break
        else:
            time.sleep(0.2)

    for channel in gpio:
        GPIO.remove_event_detect(channel)

    return True

#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

NEED_GPIO = True

build_in_trigger = \
    ['rising', 'falling', 'both']

''' func: trigger()
    '''
def trigger(channel_list, _name, params):
    edge_type = {'rising': GPIO.RISING, 'falling': GPIO.FALLING, 'both': GPIO.BOTH}

    for channel in channel_list:
        GPIO.add_event_detect(channel, edge_type[_name])

    jump = False
    while True:
        for channel in channel_list:
            if GPIO.event_detected(channel):
                jump = True
                break

        if jump:
            break
        else:
            time.sleep(0.2)

    for channel in channel_list:
        GPIO.remove_event_detect(channel)

    return True

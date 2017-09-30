#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

build_in_trigger = \
    ['rising', 'falling', 'both']

''' func: trigger()
    '''
def trigger(channel_list, _name, params):
    edge_type = {'rising': GPIO.RISING, 'falling': GPIO.FALLING, 'both': GPIO.BOTH}

    for channel in channel_list:
        GPIO.add_event_detect(channel, edge_type[_name])

    while True:
        for channel in channel_list:
            if GPIO.event_detected(channel):
                break
        else:
            time.sleep(0.2)
            continue

        break

    for channel in channel_list:
        GPIO.remove_event_detect(channel)

    return True

#!/usr/bin/env python3

import time
import random

import RPi.GPIO as GPIO

build_in_action = \
    ['turn', 'flash', 'flow', 'loop_flow', 'twinkle']

''' func: waiting()
    if duration time <= 0, use random value '''
def waiting(duration):
    if duration <= 0:
        random.seed()
        duration = random.randrange(1, 10, 1) / 10.0

    time.sleep(duration)

''' func: true2()
    output True to all channel '''
def true2(channel_list):
    for channel in channel_list:
        GPIO.output(channel, True)

''' func: false2()
    output True to all channel '''
def false2(channel_list):
    for channel in channel_list:
        GPIO.output(channel, False)

''' func: flash()
    output True and then False to all channel '''
def flash(channel_list, duration):
    true2(channel_list)
    waiting(duration)
    false2(channel_list)

''' func: turn()
    output True or False to all channel '''
def turn(channel_list):
    for channel in channel_list:
        if GPIO.input(channel) == True:
            GPIO.output(channel, False)
        else:
            GPIO.output(channel, True)

''' func: flow()
    output True/False value one by one to channel (in list)'''
def flow(channel_list, duration):
    for channel in channel_list:
        GPIO.output(channel, True)
        waiting(duration)
        GPIO.output(channel, False)

''' func: loop_flow()
    do a loop: flow()
    if total_times <= 0, can not stop '''
def loop_flow(channel_list, duration, total_times):
    while True:
        flow(channel_list, duration)

        total_times = total_times - 1
        if total_times == 0:
            break

''' func: twinkle()
    do a loop: flash()
    if total_times <= 0, can not stop '''
def twinkle(channel_list, duration, total_times):
    while True:
        flash(channel_list, duration)
        waiting(duration)

        total_times = total_times - 1
        if total_times == 0:
            break

''' func: get_times()
    '''
def get_times(times_msg):
    try:
        times = int(times_msg)
    except:
        times = 10

    return times

''' func: get_duration()
    '''
def get_duration(duration_msg):
    try:
        duration = float(duration_msg)
    except:
        duration = 0.3

    if duration == 0:
        random.seed()
        duration = random.randrange(1, 10, 1) / 10.0

    return duration

''' func: action()
    '''
def action(channel_list, _name, params):
    duration = get_duration(params[0])
    times = get_times(params[1])

    if _name == "turn":
        turn(channel_list)
    elif _name == 'flash':
        flash(channel_list, duration)
    elif _name == "flow":
        flow(channel_list, duration)
    elif _name == "loop_flow":
        loop_flow(channel_list, duration, times)
    elif _name == "twinkle":
        twinkle(channel_list, duration, times)

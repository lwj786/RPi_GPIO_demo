#!/usr/bin/env python3

import time
import random

import RPi.GPIO as GPIO

build_in_action = \
    ['turn', 'flash', 'flow', 'loop_flow', 'twinkle']

''' func: waiting()
    '''
def waiting(duration):
    time.sleep(duration)

''' func: flash()
    output True and then False to all channel '''
def flash(channel_list, duration):
    GPIO.output(channel_list, GPIO.HIGH)
    waiting(duration)
    GPIO.output(channel_list, GPIO.LOW)

''' func: turn()
    turn True/False to all channel '''
def turn(channel_list):
    channel_low, channel_high = [], []

    for channel in channel_list:
        if GPIO.input(channel) == GPIO.LOW:
            channel_low.append(channel)
        else:
            channel_high.append(channel)

    GPIO.output(channel_low, GPIO.HIGH)
    GPIO.output(channel_high, GPIO.LOW)

''' func: flow()
    output True/False value one by one to channel (in list)'''
def flow(channel_list, duration):
    for channel in channel_list:
        GPIO.output(channel, GPIO.HIGH)
        waiting(duration)
        GPIO.output(channel, GPIO.LOW)

''' func: loop_flow()
    do a loop: flow() '''
def loop_flow(channel_list, duration, total_times):
    for i in range(total_times):
        flow(channel_list, duration)

''' func: twinkle()
    do a loop: flash() '''
def twinkle(channel_list, duration, total_times):
    for i in range(total_times):
        flash(channel_list, duration)
        waiting(duration)

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
    if len(params) < 2:
        params.extend([0.3, 10][(len(params) - 2):])

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

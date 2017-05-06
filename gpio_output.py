#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import random

''' func: waiting()
    if duration time <= 0, use random value '''
def waiting(duration):
    if duration <= 0:
        random.seed()
        duration = random.randrange(1, 10, 1) / 10.0

    time.sleep(duration)

''' func: true()
    output True to all gpio header '''
def true2(gpio_OUT):
    for gpio in gpio_OUT:
        GPIO.output(gpio, True)

''' func: false()
    output True to all gpio header '''
def false2(gpio_OUT):
    for gpio in gpio_OUT:
        GPIO.output(gpio, False)

''' func: flash()
    output True and then False to all gpio header '''
def flash(gpio_OUT, duration):
    true2(gpio_OUT)
    waiting(duration)
    false2(gpio_OUT)

''' func: turn()
    output True or False to all gpio header '''
def turn(gpio_OUT):
    for gpio in gpio_OUT:
        if GPIO.input(gpio) == True:
            GPIO.output(gpio, False)
        else:
            GPIO.output(gpio, True)

''' func: flow()
    output True/False value one by one to gpio header (in list) '''
def flow(gpio_OUT, duration):
    for gpio in gpio_OUT:
        GPIO.output(gpio, True)
        waiting(duration)
        GPIO.output(gpio, False)

''' func: loop_flow()
    do a loop: flow()
    if total_times <= 0, can not stop '''
def loop_flow(gpio_OUT, duration, total_times):
    while True:
        flow(gpio_OUT, duration)

        total_times = total_times - 1
        if total_times == 0:
            break

''' func: twinkle()
    do a loop: flash()
    if total_times <= 0, can not stop '''
def twinkle(gpio_OUT, duration, total_times):
    while True:
        flash(gpio_OUT, duration)
        waiting(duration)

        total_times = total_times - 1
        if total_times == 0:
            break

#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
import random
import threading

import gpio_output as GO
from gpio_input import wait_for_trigger

''' func: behavior()
    do operation as the behavior setted, default "flash" '''
def behavior(scheme):
    if scheme['behavior'] == "turn":
        GO.turn(scheme['out'])
    elif scheme['behavior'] == "flow":
        GO.flow(scheme['out'], scheme['duration'])
    elif scheme['behavior'] == "loop_flow":
        GO.loop_flow(scheme['out'], scheme['duration'], scheme['times'])
    elif scheme['behavior'] == "twinkle":
        GO.twinkle(scheme['out'], scheme['duration'], scheme['times'])
    else:
        GO.flash(scheme['out'], scheme['duration'])

''' func: action
    wait for specific input to trigger behavior '''
def action(scheme):
    if len(scheme['in']) != 0:
        while True:
            if wait_for_trigger(scheme['in'], scheme['trigger']):
                behavior(scheme)
    else:
        behavior(scheme)

''' func: comfirm()
    comfirm query '''
def comfirm(hint, ToF):
    if raw_input(hint) == ToF:
        return True

    return False

''' func: print_scheme_message()
    '''
def print_scheme_message(scheme_list):
    count = 1

    for scheme in scheme_list:
        print("* scheme " + str(count))
        count = count + 1

        print("ouput: "+ str(len(scheme['out'])))
        print(scheme['out'])
        print("output behavior: " + scheme['behavior'])
        print("duration: " + str(scheme['duration']))
        print("times(not time): " + str(scheme['times']))

        print("input: "+ str(len(scheme['in'])))
        print(scheme['in'])
        print("trigger condition: " + scheme['trigger'])


''' func: gpio_setup()
    '''
def gpio_setup(scheme_list):
    for scheme in scheme_list:
        GPIO.setup(scheme['out'], GPIO.OUT)
        GPIO.setup(scheme['in'], GPIO.IN)

''' func: get_trigger_mode()
    '''
def get_trigger_mode(trigger):
    trigger_list = \
        ['rising', 'falling', 'both']

    if trigger in trigger_list:
        return trigger

    return 'rising'

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

''' func: get_behavior_mode
    '''
def get_behavior_mode(behavior):
    behavior_list = \
        ['flash', 'turn', 'flow', 'loop_flow', 'twinkle']

    if behavior in behavior_list:
        return behavior

    return 'flash'

''' func: check_gpio
    check the validity of gpio which might be used '''
def check_gpio(gpio_code):
    GENERAL_GPIO_BCM_CODE = \
        [4, 17, 18, 27, 22, 23, 24, 25, 5, 6, 12, 13, 19, 16, 26, 20, 21]

    for code in GENERAL_GPIO_BCM_CODE:
        if gpio_code == str(code):
            return True

    return False

''' func: get_gpio()
    get gpio in use '''
def get_gpio(gpio_msg_list):
    gpio_list = []

    for gpio in gpio_msg_list:
        if  check_gpio(gpio):
            gpio_list.append(int(gpio))

    return gpio_list

''' func: get_scheme()
    get scheme from scheme_msg '''
def get_scheme(scheme_msg):
    scheme_list = []

    for msg in scheme_msg:
        scheme = {
            'out': [], 'behavior': 'flash', 'duration': 0.3, 'times': 10,
            'in': [], 'trigger': 'rising'
        }

        msg = msg.split(':')
        if len(msg) == 1 or len(msg) == 2:
            try:
                scheme['out'] = get_gpio(msg[0].split('=')[0].split(','))
            except:
                scheme['out'] = []

            try:
                scheme['behavior'] = get_behavior_mode(msg[0].split('=')[1].split('/')[0])
            except:
                scheme['behavior'] = 'flash'

            try:
                scheme['duration'] = get_duration(msg[0].split('=')[1].split('/')[1].split(',')[0])
            except:
                scheme['duration'] = 0.3

            try:
                scheme['times'] = get_times(msg[0].split('=')[1].split('/')[1].split(',')[1])
            except:
                scheme['times'] = 10

            if len(msg) == 2:
                try:
                    scheme['in'] = get_gpio(msg[1].split('=')[0].split(','))
                except:
                    scheme['in'] = []

                try:
                    scheme['trigger'] = get_trigger_mode(msg[1].split('=')[1])
                except:
                    scheme['trigger'] = 'rising'
        else:
            continue

        scheme_list.append(scheme)

    return scheme_list

''' func: help()
    '''
def help():
    print("-h, --help")
    print("-y disable the comfirm query")
    print("--scheme-... a scheme is a config to set GPIO and it's function")
    print("\tformat: gpio_code=behavior_mode/duration,times:gpio_code=trigger_mode")
    print("\t-firt part (before ':'), sets gpio for output")
    print("\t * gpio_code -- like 23,24,25")
    print("\t * behavior mode: i) the output behavior of single header or ii) behavior(relationship) of all of headers")
    print("\t     1) flash: output True and then False 2) turn: if True then False, or opposite")
    print("\t     3) flow: flash the header one by one 4) loop_flow: loop the flow (if times <= 0, won't stop)")
    print("\t     5) twinkle: loop the flash (if times <= 0, won't stop)")
    print("\t * duration -- sets the duration of single output, default value: 0.3")
    print("\t     define <=0 as random duration(while <0 it's real-time duration), random range (0:0.1:1)")
    print("\t * times -- sets the times(not time) of repeating output behavior(work for repetitive mode), default value: 10")
    print("\t-second part, sets gpio for input")
    print("\t * gpio_code -- same as above")
    print("\t * trigger_mode: use edge detection, if it fits the condition then trigger")
    print("\t     1) rising  2) falling 3) both")
    print("\texample: 23,24,25=twinkle/0.1,30:21=rising")

    exit()

''' begin
    '''
# initialize
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# process argv
comfirm_setting = "enable"
scheme_msg = []
for arg in sys.argv:
    if arg[:len("--scheme-")] == "--scheme-":
        scheme_msg.append(arg[len("--scheme-"):])
    elif arg == "-y":
        comfirm_setting = "disable"
    elif arg == "-h" or arg == "--help":
        help()

# get scheme and setup gpio
scheme_list = get_scheme(scheme_msg)
gpio_setup(scheme_list)

# print message
print_scheme_message(scheme_list)

# perform the operation
if comfirm_setting == "disable" or \
    comfirm('***PLEASE CHECK IT !!! [Y/n]*** :', 'Y') == True:
    print("...")

    for scheme in scheme_list:
        t = threading.Thread(target = action, args = (scheme, ))
        t.setDaemon(True)
        t.start()
else:
    exit()

while True:
    if raw_input(">> ") == "exit":
        break

# clean up
GPIO.cleanup()

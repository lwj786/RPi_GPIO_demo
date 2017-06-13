#!/usr/bin/env python3

import RPi.GPIO as GPIO
import sys
import random
import threading

import gpio_output as GO
import gpio_input as GI
import stdio_manager as siom

global EI, EO

''' func: behave()
    '''
def behave(scheme):
    if scheme['behavior'] in GO.build_in_behavior \
        or scheme['behavior'] == []:
        GO.behavior(scheme['out'], scheme['behavior'], scheme['behavior_params'])
    else:
        module = scheme['behavior']
        try:
            EO = __import__(module)
            EO.behavior(scheme['out'], scheme['behavior_params'])
        except:
            return

''' func: action()
    wait for specific input to trigger behavior '''
def action(scheme):
    if scheme['trigger'] in GI.build_in_trigger \
        or scheme['trigger'] == []:
        wait_for_trigger = GI.trigger
        arg = scheme['trigger']
    else:
        module = scheme['trigger']
        try:
            EI = __import__(module)
            wait_for_trigger = EI.trigger
            arg = scheme['trigger_params']
        except:
            return

    if len(scheme['in']) != 0:
        while True:
            if wait_for_trigger(scheme['in'], arg):
                behave(scheme)
    else:
        behave(scheme)

''' func: comfirm()
    comfirm query '''
def comfirm(hint, ToF):
    if input(hint) == ToF:
        return True

    return False

''' func: print_scheme_message()
    '''
def print_scheme_message(scheme_list):
    count = 1

    for scheme in scheme_list:
        print("* scheme " + str(count))
        count = count + 1

        print("    ouput: "+ str(len(scheme['out'])))
        print("    ", end = "")
        print(scheme['out'])
        print("    output behavior: " + scheme['behavior'])
        print("    behavior parameter: ")
        print("    ", end = "")
        print(scheme['behavior_params'])
        print("    input: "+ str(len(scheme['in'])))
        print("    ", end = "")
        print(scheme['in'])
        print("    trigger condition: " + scheme['trigger'])
        print("    trigger parameter: ")
        print("    ", end = "")
        print(scheme['trigger_params'])

''' func: gpio_setup()
    '''
def gpio_setup(scheme_list):
    for scheme in scheme_list:
        GPIO.setup(scheme['out'], GPIO.OUT)
        GPIO.setup(scheme['in'], GPIO.IN)

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
            'out': [], 'behavior': 'flash', 'behivior_params': [],
            'in': [], 'trigger': 'rising', 'trigger_params': []
        }

        msg = msg.split(':')
        try:
            scheme['out'] = get_gpio(msg[0].split('=')[0].split(','))
        except:
            scheme['out'] = []
        try:
            scheme['behavior'] = msg[0].split('=')[1].split('/')[0]
        except:
            scheme['behavior'] = 'flash'
        try:
            scheme['behavior_params'] = msg[0].split('=')[1].split('/')[1].split(',')
        except:
            scheme['behavior_params'] = []

        try:
            scheme['in'] = get_gpio(msg[1].split('=')[0].split(','))
        except:
            scheme['in'] = []
        try:
            scheme['trigger'] = msg[1].split('=')[1].split('/')[0]
        except:
            scheme['trigger'] = 'rising'
        try:
            scheme['trigger_params'] = msg[1].split('=')[1].split('/')[1].split(',')
        except:
            scheme['trigger_params'] = []

        scheme_list.append(scheme)

    return scheme_list

''' func: help()
    '''
def help():
    help_content = '''-h, --help
-y disable the comfirm query
--scheme-... a scheme is a config to set GPIO and it's function
\tformat: gpio_code=behavior_mode/param_list:gpio_code=trigger_mode/param_list
\t-firt part (before ':'), sets gpio for output
\t * gpio_code -- like 23,24,25
\t * build-in behavior mode: i) the output behavior of single header or ii) behavior(relationship) of all of headers
\t     1) flash: output True and then False 2) turn: if True then False, or opposite
\t     3) flow: flash the header one by one 4) loop_flow: loop the flow (if times <= 0, won't stop)
\t     5) twinkle: loop the flash (if times <= 0, won't stop)
\t * param_list -- like arg0,arg1,arg2
\t     for build-in behavior, the parameters is duration and/or times
\t     # duration -- sets the duration of single output, default value: 0.3
\t         define <=0 as random duration(while <0 it's real-time duration), random range (0:0.1:1)
\t     # times -- sets the times(not time) of repeating output behavior(work for repetitive mode), default value: 10
\t-second part, sets gpio for input
\t * gpio_code -- same as above
\t * build-in trigger_mode: use edge detection, if it fits the condition then trigger
\t     1) rising  2) falling 3) both
\t   for build-in trigger mode, there is no parameters
\texample: 23,24,25=twinkle/0.1,30:21=rising'''

    print(help_content)
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

# standard I/O management for multi-process
siom.main()

# clean up
GPIO.cleanup()

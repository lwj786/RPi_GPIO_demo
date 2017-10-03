#!/usr/bin/env python3

import sys
import random
import threading

import RPi.GPIO as GPIO

import build_in_input as GI
import build_in_output as GO
import stdio_manager as siom

EXPLANATION = \
'''-h, --help
-y disable the comfirm query
--add-path=/path/to/file add path to sys.path
other parameters will be treated as scheme, a scheme is a config to set GPIO and it's function,
\tis a description to behavior which consists of trigger and action
\tformat: channel^param_list@trigger:channel^param_list@action
\t-firt part (before ':'), sets gpio for input
\t * channel -- gpio code(BCM), like 21
\t * param_list -- like arg0,arg1,arg2
\t     for build-in trigger, there is no parameter
\t * trigger -- define the trigger condition
\t     build-in trigger: use edge detection, 1) rising 2) falling 3) both
\t     default 1)
\t-second part, sets gpio for output
\t * channel -- see ibid
\t * param_list -- see ibid
\t     for build-in behavior, the parameters is duration and/or times
\t     # duration -- sets the duration of single output, default value: 0.3
\t         define =0 as random duration, random range (0:0.1:1)
\t     # times -- sets the times(not time) of repeating output behavior(work for repetitive mode), default value: 10
\t * action -- implement i) the output state and it's change of header
\t      or ii) the relationship of different headers' states and their change
\t     built-in action:
\t     1) flash: output True and then False; 2) twinkle: loop the flash;
\t     3) flow: flash the header one by one; 4) loop_flow: loop the flow;
\t     5) turn: if True then False, or opposite
\t     default 1)
\texample: 21^@rising:23,24,25^0.3,10@twinkle or just 21^:23,24,25^twinkle'''

GENERAL_GPIO_BCM_CODE = \
    [4, 17, 18, 27, 22, 23, 24, 25, 5, 6, 12, 13, 19, 16, 26, 20, 21]

''' func: behavior()
    wait for specific input to trigger action '''
def behavior(scheme):
    # setup trigger
    if scheme['trigger'] not in GI.build_in_trigger:
        try:
            TRIGGER = __import__(scheme['trigger'])
        except:
            return
    else:
        TRIGGER = GI

    wait_for_trigger = TRIGGER.trigger
    need_gpio = not hasattr(TRIGGER, "NO_NEED_GPIO")

    # setup action
    if scheme['action'] not in GO.build_in_action:
        try:
            ACTION = __import__(scheme['action'])
        except:
            return
    else:
        ACTION = GO

    act = ACTION.action

    if len(scheme['in']) == 0 and need_gpio:
        act(scheme['out'], scheme['action'], scheme['action_params'])
    else:
        while True:
            if wait_for_trigger(scheme['in'], scheme['trigger'], scheme['trigger_params']):
                act(scheme['out'], scheme['action'], scheme['action_params'])

''' func: comfirm()
    '''
def comfirm(hint, yes):
    if input(hint) == yes:
        return True

    return False

''' func: print_scheme_message()
    '''
def print_scheme_message(scheme_list):
    for i, scheme in enumerate(scheme_list):
        print(' '.join(["* scheme", str(i + 1)]))

        print(' '.join(["\tinput:", str(len(scheme['in']))]))
        print('\t', end = '')
        print(scheme['in'])

        print(' '.join(["\ttrigger condition:", scheme['trigger']]))
        print("\ttrigger parameter: ")
        print('\t', end = '')
        print(scheme['trigger_params'])

        print(' '.join(["\toutput:", str(len(scheme['out']))]))
        print("\t", end = '')
        print(scheme['out'])

        print(' '.join(["\toutput action:", scheme['action']]))
        print("\taction parameter: ")
        print('\t', end = '')
        print(scheme['action_params'])

''' func: gpio_setup()
    '''
def gpio_setup(scheme_list):
    for scheme in scheme_list:
        GPIO.setup(scheme['in'], GPIO.IN)
        GPIO.setup(scheme['out'], GPIO.OUT)

''' func: check_channel
    check the validity of channel code '''
def check_channel(channel_code):
    for code in GENERAL_GPIO_BCM_CODE:
        if channel_code == str(code):
            return True

    return False

''' func: get_channel_list()
    '''
def get_channel_list(channel_msg):
    channel_list = []

    for channel in channel_msg:
        if  check_channel(channel):
            channel_list.append(int(channel))

    return channel_list

''' func: get_scheme()
    '''
def get_scheme(scheme_msg):
    scheme_list = []

    for msg in scheme_msg:
        scheme = {
            'in': [], 'trigger': '', 'trigger_params': [],
            'out': [], 'action': '', 'behivior_params': []
        }

        msg = msg.split(':')

        try:
            scheme['in'] = get_channel_list(msg[0].split('^')[0].split(','))
        except:
            scheme['in'] = []
        try:
            scheme['trigger_params'] = msg[0].split('^')[1].split('@')[0].split(',')
        except:
            scheme['trigger_params'] = []
        try:
            scheme['trigger'] = msg[0].split('^')[1].split('@')[1]
        except:
            scheme['trigger'] = ''

        if len(scheme['in']) and not len(scheme['trigger']):
            scheme['trigger'] = 'rising'

        try:
            scheme['out'] = get_channel_list(msg[1].split('^')[0].split(','))
        except:
            scheme['out'] = []
        try:
            scheme['action_params'] = msg[1].split('^')[1].split('@')[0].split(',')
        except:
            scheme['action_params'] = []
        try:
            scheme['action'] = msg[1].split('^')[1].split('@')[1]
        except:
            scheme['action'] = ''

        if len(scheme['out']) and not len(scheme['action']):
            scheme['action'] = 'flash'

        if len(scheme['trigger']) and len(scheme['action']):
            scheme_list.append(scheme)

    return scheme_list

''' func: explain()
    '''
def explain():
    print(EXPLANATION)
    exit()

''' begin
    '''
# initialize
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# process argv
comfirm_setting = "enable"
scheme_msg = []

sys.argv.pop(0)
for arg in sys.argv:
    if arg[:len("--add-path=")] == "--add-path=":
        sys.path.append(arg[len("--add-path="):])
    elif arg == "-y":
        comfirm_setting = "disable"
    elif arg == "-h" or arg == "--help":
        explain()
    else:
        scheme_msg.append(arg)

if not len(scheme_msg):
    explain()

# get scheme and setup gpio
scheme_list = get_scheme(scheme_msg)
gpio_setup(scheme_list)

# print message
print_scheme_message(scheme_list)

# perform the operation
if comfirm_setting == "disable" or \
    comfirm('***PLEASE CHECK IT !!! [Y/n]*** :', 'Y') == True:

    for scheme in scheme_list:
        t = threading.Thread(target = behavior, args = (scheme, ))
        t.setDaemon(True)
        t.start()
else:
    GPIO.cleanup()
    exit()

# standard I/O management for multi-process
siom.main()

# clean up
GPIO.cleanup()

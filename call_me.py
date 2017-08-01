#!/usr/bin/env python3

import stdio_manager as siom

NEED_GPIO = False

''' func: trigger()
    interface for demo.py, trigger condition: standard input '''
def trigger(channel_list, _name, params):
    name = "me"

    for parameter in params:
        if parameter[:7] == "--name-":
            name = parameter[7:]

    index = siom.register(name)

    while True:
        if siom.pull_input(index) == name:
            break

    siom.push_output("be triggered", index)
    siom.unregister(index)

    return True

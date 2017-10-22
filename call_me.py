#!/usr/bin/env python3

import stdio_manager as siom

NO_NEED_GPIO = True

''' func: trigger()
    interface for demo.py, trigger condition: standard input '''
def trigger(channel_list, _name, params):
    if len(params):
        name = ' '.join(params)

    if not len(name):
        name = _name[-2:]

    index = siom.register(name)

    while True:
        if siom.pull_input(index) == name:
            break

    siom.push_output("be triggered", index)
    siom.unregister(index)

    return True

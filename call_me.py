#!/usr/bin/env python3

import stdio_manager as siom

NEED_GPIO = 0

def trigger(gpio_list, params_list):
    name = "me"

    for parameter in params_list:
        if parameter[:7] == "--name-":
            name = parameter[7:]

    index = siom.register(name)

    while True:
        if siom.pull_input(index) == name:
            break

    siom.push_output("be triggered", index)
    siom.unregister(index)

    return True

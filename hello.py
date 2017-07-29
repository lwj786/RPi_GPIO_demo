#!/usr/bin/env python3

import stdio_manager as siom

def hello(string):
    if len(string) == 0:
        string = "World"

    print(" ".join(["Hello", string, "!"]))

def main(string_list):
    hello(" ".join(string_list))

def action(gpio_list, _name, params_list):
    global print

    name = "hello"
    content_list = []
    for parameter in params_list:
        if parameter[:7] == "--name-":
            name = parameter[7:]
        else:
            content_list.append(parameter)

    def output_with_identity(index):
        def push_output(content):
            siom.push_output(content, index)

        return push_output

    index = siom.register(name)
    print = output_with_identity(index)

    main(content_list)

    siom.unregister(index)

if __name__ == "__main__":
    from sys import argv

    main(argv[1:])

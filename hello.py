#!/usr/bin/env python3

import stdio_manager as siom

def hello(string):
    if len(string) == 0:
        string = "World"

    print(" ".join(["Hello", string, "!"]))

def main(string_list):
    hello(" ".join(string_list))

''' func: action()
    interface for demo.py, output: standard output '''
def action(channel_list, _name, params):
    global print

    name = "hello"
    content_list = []
    for parameter in params:
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

''' begin
    '''
if __name__ == "__main__":
    from sys import argv

    main(argv[1:])

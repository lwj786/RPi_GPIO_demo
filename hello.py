#!/usr/bin/env python3

import stdio_manager as siom

def hello(string):
    if len(string):
        string = "World"

    print(' '.join(["Hello", string, "!"]))

def main(string_list):
    hello(' '.join(string_list))

''' func: action()
    interface for demo.py, output: standard output '''
def action(channel_list, _name, params):
    global print

    index = siom.register(_name)
    print = lambda content: siom.push_output(content, index)

    main(params)

    siom.unregister(index)

''' begin
    '''
if __name__ == "__main__":
    from sys import argv

    main(argv[1:])

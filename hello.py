#!/usr/bin/env python3

def hello(string):
    if len(string) == 0:
        string = "World"

    print(" ".join(["Hello", string, "!"]))

def main(string_list):
    hello(" ".join(string_list))

def behavior(gpio_list, params_list):
    main(params_list)

if __name__ == "__main__":
    from sys import argv

    main(argv[1:])

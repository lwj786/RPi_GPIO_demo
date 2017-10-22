#!/usr/bin/env python3

import threading
import sys
import time

LOCK = threading.Lock()

USER = {'name': [], 'idle_index': []}
IO = {
    'input': "", 'input_status': [],
    'output': [], 'output_status': False # outout's element is [index, content]
}

''' push_output(), pull_input(), register(), unregister() is for other sub-thread
    for input, it's necessary to use register() and good to use unregister()
    '''
def push_output(output_content, index = -1):
    global IO

    LOCK.acquire()
    try:
        IO['output'].append([index, output_content])
        IO['output_status'] = True
    finally:
        LOCK.release()

def pull_input(index):
    global IO

    while True:
        if IO['input_status'][index]:
            LOCK.acquire()
            try:
                input_content = IO['input']
                IO['input_status'][index] = False
            finally:
                LOCK.release()

            break
        else:
            time.sleep(0.2)

    return input_content

def register(name = ""):
    global USER, IO

    LOCK.acquire()
    try:
        if len(USER['idle_index']):
            index = USER['idle_index'].pop()
        else:
            IO['input_status'].append(False)
            index = len(IO['input_status']) - 1

        if not len(name):
            name = str(index)

        if index < len(USER['name']):
            USER['name'][index] = name
        else:
            USER['name'].append(name)
    finally:
        LOCK.release()

    return index

def unregister(index):
    global USER

    LOCK.acquire()
    try:
        USER['idle_index'].append(index)
    finally:
        LOCK.release()

''' main(), output() for main thread
    '''
def main(prompt = ">> ", exit_flag = "exit"):
    global IO

    print(exit_flag.join(["input ", " to exit !"]))

    # put output() to daemon
    def output(prompt):
        global USER, IO

        while True:
            if IO['output_status']:
                LOCK.acquire()
                try:
                    print("")
                    for [index, content] in IO['output']:
                        if index + 1:
                            identity = ''.join([str(index), "-", USER['name'][index], ":"])
                            print(identity)

                        print(content)

                    print(prompt, end = "")
                    sys.stdout.flush()

                    del IO['output'][:]
                    IO['output_status'] = False
                finally:
                    LOCK.release()
            else:
                time.sleep(0.2)

    output_thread = threading.Thread(target = output, args = (prompt, ))
    output_thread.setDaemon(True)
    output_thread.start()

    # input
    while True:
        input_content = input(prompt)
        if input_content == exit_flag:
            break
        else:
            LOCK.acquire()
            try:
                IO['input'] = input_content
                IO['input_status'] = [True for i in IO['input_status']]
            finally:
                LOCK.release()

    if __name__ == "__main__":
        exit()
    else:
        return

''' begin
    '''
if __name__ == "__main__":
    main()

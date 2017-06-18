#!/usr/bin/env python3

import threading
import sys
import time

LOCK = threading.Lock()

USER_NAME = []
IDLE_USER = []

INPUT_CONTENT = ""
INPUT_STATUS = []    # 1 -- has updated

OUTPUT_CONTENT = []    # element is [index, content]
OUTPUT_STATUS = 0

''' push_output(), pull_input(), register(), unregister() is for other sub-thread
    for input, it's necessary to use register() and good to use unregister()
    '''
def push_output(output_content, index = -1):
    global OUTPUT_CONTENT, OUTPUT_STATUS

    LOCK.acquire()
    try:
        OUTPUT_CONTENT.append([index, output_content])
        OUTPUT_STATUS = 1
    finally:
        LOCK.release()

def pull_input(index):
    global INPUT_STATUS, INPUT_CONTENT

    while True:
        if INPUT_STATUS[index]:
            LOCK.acquire()
            try:
                input_content = INPUT_CONTENT
                INPUT_STATUS[index] = 0
            finally:
                LOCK.release()

            break
        else:
            time.sleep(0.2)

    return input_content

def register(name = ""):
    global IDLE_USER, INPUT_STATUS, USER_NAME

    LOCK.acquire()
    try:
        if len(IDLE_USER):
            index = IDLE_USER.pop()
        else:
            INPUT_STATUS.append(0)
            index = len(INPUT_STATUS) - 1

        if name == "":
            name = str(index)

        if index < len(USER_NAME):
            USER_NAME[index] = name
        else:
            USER_NAME.append(name)
    finally:
        LOCK.release()

    return index

def unregister(index):
    global IDLE_USER

    LOCK.acquire()
    try:
        IDLE_USER.append(index)
    finally:
        LOCK.release()

''' main(), output() for main thread
    '''
def main(prompt = ">> ", exit_flag = "exit"):
    global INPUT_CONTENT, INPUT_STATUS

    print(exit_flag.join(["input ", " to exit !"]))

    # put output() to daemon
    def output(prompt):
        global OUTPUT_STATUS, OUTPUT_CONTENT, USER_NAME

        while True:
            if OUTPUT_STATUS:
                LOCK.acquire()
                try:
                    print("")
                    for output_content in OUTPUT_CONTENT:
                        if output_content[0] + 1:
                            identity = str(output_content[0]) + "-" \
                                + USER_NAME[output_content[0]] + ":"
                            print(identity)

                        print(output_content[1])

                    print(prompt, end = "")
                    sys.stdout.flush()

                    del OUTPUT_CONTENT[:]
                    OUTPUT_STATUS = 0
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
                INPUT_CONTENT = input_content

                for i in range(len(INPUT_STATUS)):
                    INPUT_STATUS[i] = 1
            finally:
                LOCK.release()

    if __name__ == "__main__":
        exit()
    else:
        return

if __name__ == "__main__":
    main()

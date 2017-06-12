#!/usr/bin/env python3

import time
import threading

LOCK = threading.Lock()

INPUT_CONTENT = ""
INPUT_STATUS = []    # 1 -- has updated

def get_input(index):
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

def register():
    global INPUT_STATUS

    LOCK.acquire()
    try:
        INPUT_STATUS.append(0)
        index = len(INPUT_STATUS) - 1
    finally:
        LOCK.release()

    return index

def main(prompt = ">> ", exit_flag = "exit"):
    global INPUT_CONTENT, INPUT_STATUS

    print(exit_flag.join(["input ", " to exit !"]))

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

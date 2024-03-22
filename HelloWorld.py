import pyads
import os
import random
import time

# function to clear the screen
def clear():
    os.system('cls')

# clear the screen
# clear()

# title
print("PYADS Quick Start")
print("-------------------")

# connection
plc = pyads.Connection('192.168.1.15.1.1', 851)
plc.open()

VAR_NAME = 'GVL.rAIInput1'
VAR2_NAME = 'GVL.rAIInput2'
RUN = True

while RUN :
    # read test
    readResult = plc.read_by_name(VAR_NAME)
    readResult2 = plc.read_by_name(VAR2_NAME)

    # print the result with 2 decimal places
    print(f"{readResult:.2f} {readResult2:.2f}", end="\r")
    # wait
    time.sleep(0.01)

plc.close()
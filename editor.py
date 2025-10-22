import curses
import sys

RIGHT_KEYS = set("qwertasdfgzxcvb12345`~!@#$%^&*()-_=+\\|")
LEFT_KEYS = set("yuiophjklnm67890[]{};:'\",.<>/?")

OPCODES = {
    "00000001": "set [1] to value of address [2]",
    "00000010": "read from user 1 bit into [1]",
    "00000011": "write [1]",
    "00000100": "set [1] to value of [2]",
    "00010100": "add [2] + [3] and place it in [1]",
    "00011100": "multiply [2] * [3] and place it in [1]",
    "00011000": "subtract [2] - [3] and place it in [1]",
    "00011010": "divide [2] / [3] and place it in [1]",
    "00100001": "if [0] == [1] goto [2]",
    "00100010": "if [0] >= [1] goto [2]",
    "00100011": "if [0] <= [1] goto [2]",
    "00100110": "if [0] > [1] goto [2]",
    "00100111": "if [0] < [1] goto [2]",
    "00100101": "if [0] != [1] goto [2]",
    "00001111": "run from memory [1] with args memory[2:]",
    "00001010": "load from persistent byte persistent[1] to memory[2]",
    "00010101": "write to persistent memory memory[1] -> persistent[memory[2]]",
    "01000000": "goto line [1] and run from there",
    "01011111": "thread: start line [0], end line [1], time [2]", 
    "01001010":"pause for [1] secconds"
}
print("editor has been removed and tkurses will be used to make it later")

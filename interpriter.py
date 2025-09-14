import time
import sys
import lineExecuter as le
import globalVar as gv

if sys.platform.startswith('win'):
    import msvcrt

    def read_char():
        char = msvcrt.getch().decode()
        print(char, end='', flush=True)
        return char

else:
    import tty
    import termios

    def read_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print(ch, end='', flush=True)
        return ch

def write_fixed_line(filename, line_num, value):
    with open(filename, 'r+b') as file:
        offset = line_num * 9  # 8 bits + newline
        file.seek(offset)
        file.write((value + '\n').encode())



def createMemoryFile(bytes):
    with open("memory.bhm", "w") as file:
        for i in range(bytes):
            file.write("00000000\n")
line_executer = le.executor()
def interprit(code, arg=None, o44=False):
    gv.code=code
    if arg is not None:
        gv.memory[int("10000000",2)] = arg
    newCode=code.split("\n")
    while gv.currentLine < len(newCode):
        if o44==True:
            gv.currentLine=0
        time.sleep(0.01)
        line = newCode[gv.currentLine]
        line_executer.execute_line(line)

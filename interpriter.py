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
def interprit(code, arg=None, o44=False):
    line_executer = le.Executor()
    gv.code=code
    newCode=code.split("\n")
    while gv.currentLine < len(newCode):
        if o44==True:
            gv.currentLine=0
        time.sleep(0.01)
        line = newCode[gv.currentLine]
        line_executer.execute_line(line)
    if (gv.debug):
        print("\n----program end----")
    if (gv.pref):
        line_executer.endTime = time.time()
        print("time and performance")
        print(f"totalTime {line_executer.endTime-line_executer.startTime}")
        for line, start,end in zip(line_executer.processes, line_executer.startTimesProccesses, line_executer.endTimesProccesses):
            print(f"     proccess {line}: time: {end-start:.10f}")


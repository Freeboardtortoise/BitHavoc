import time
import sys

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


memory = [''] * 10000000
functions = []
currentLine = 0
def createMemoryFile(bytes):
    with open("memory.bhm", "w") as file:
        for i in range(bytes):
            file.write("00000000\n")

def interprit(code, arg=None):
    global functions, memory, currentLine
    if arg is not None:
        memory[int("100000",2)] = arg
    newCode=code.split("\n")
    while currentLine < len(newCode):
        time.sleep(0.01)
        line = newCode[currentLine]
        if len(" ".join(line)) < 7:
            currentLine+=1
            continue
        line = line.split(" ")
        if line[0] == "000001":
            memory[int(line[1], 2)] = memory[int(line[2], 2)]
        elif line[0] == "000010":
            memory[int(line[1], 2)] = "0"+bin(ord(read_char()))[2:]
        elif line[0] == "000011":
            address = int(line[1], 2)
            print(chr(int(memory[address],2)), end='', flush=True)
        elif line[0] == "000100":
            memory[int(line[1],2)] = line[2]

        # mathamatical operations
        elif line[0] == "010100":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) + int(memory[int(line[3],2)],2)
        elif line[0] == "011100":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) * int(memory[int(line[3],2)],2)
        elif line[0] == "011000":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) - int(memory[int(line[3],2)],2)
        elif line[0] == "011010":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) / int(memory[int(line[3],2)],2)
        elif line[0] == "110001":
            functions.append([line[1],line[2:]])
        currentLine+=1

        if line[0][0] == "1": #if statements
            if line[0] == "100001":
                if memory[int(line[1], 2)] == memory[int(line[2], 2)]:
                    currentLine=int(line[3], 2)
                    print(f"goto {int(line[3], 2)}")
            elif line[0] == "100010":
                if memory[int(line[1],2)] >= memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100011":
                if memory[int(line[1],2)] <= memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100110":
                if memory[int(line[1],2)] > memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100111":
                if memory[int(line[1],2)] < memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100101":
                if memory[int(line[1],2)] != memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
        elif line[0] == "001010":  # reading a specific line from file
            target_line = int(memory[int(line[1], 2)], 2)
            result = '00000000'  # default value if line not found

            with open("memory.bhm", "r") as file:
                for current_line_number, line_text in enumerate(file):
                    if current_line_number == target_line:
                        result = line_text.strip()
                        break  # stop reading file once we get our line

            memory[int(line[2], 2)] = result

        elif line[0] == "010101": #writing to memory
            whatToWrite=memory[int(line[1], 2)]
            where = int(line[2],2)
            print(f"writing {whatToWrite} to {where}")
            with open("memory.bhm", "r") as file:
                file_contents = file.read().splitlines()

            file_contents[where] = whatToWrite

            with open("memory.bhm", "w") as file:
                file.write("\n".join(file_contents) + "\n")
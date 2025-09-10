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

def interprit(code, arg=None, o44=False):
    global functions, memory, currentLine
    if arg is not None:
        memory[int("10000000",2)] = arg
    newCode=code.split("\n")
    while currentLine < len(newCode):
        if o44==True:
            currentLine=0
        time.sleep(0.01)
        line = newCode[currentLine]
        if len(" ".join(line)) < 7:
            currentLine+=1
            continue
        line = line.split(" ")
        print(line)
        if line[0] == "00000001":
            memory[int(line[1], 2)] = memory[int(line[2], 2)]
        elif line[0] == "00000010":
            memory[int(line[1], 2)] = "0"+bin(ord(read_char()))[2:]
        elif line[0] == "00000011":
            address = int(line[1], 2)
            print(chr(int(memory[address],2)), end='', flush=True)
        elif line[0] == "00000100":
            memory[int(line[1],2)] = line[2]

        # mathamatical operations
        elif line[0] == "00010100":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) + int(memory[int(line[3],2)],2)
        elif line[0] == "00011100":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) * int(memory[int(line[3],2)],2)
        elif line[0] == "00011000":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) - int(memory[int(line[3],2)],2)
        elif line[0] == "00011010":
            memory[int(line[1],2)] = int(memory[int(line[2],2)],2) / int(memory[int(line[3],2)],2)
        elif line[0] == "00110001":
            functions.append([line[1],line[2:]])
        currentLine+=1

        if line[0][0] == "1": #if statements
            if line[0] == "00100001":
                if memory[int(line[1], 2)] == memory[int(line[2], 2)]:
                    currentLine=int(line[3], 2)
                    print(f"goto {int(line[3], 2)}")
            elif line[0] == "00100010":
                if memory[int(line[1],2)] >= memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "00100011":
                if memory[int(line[1],2)] <= memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "00100110":
                if memory[int(line[1],2)] > memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "00100111":
                if memory[int(line[1],2)] < memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "00100101":
                if memory[int(line[1],2)] != memory[int(line[2],2)]:
                    currentLine=int(line[3], 2)
        elif line[0] == "00001010":  # reading a specific line from file
            target_line = int(memory[int(line[1], 2)], 2)
            result = '00000000'  # default value if line not found

            with open("memory.bhm", "r") as file:
                for current_line_number, line_text in enumerate(file):
                    if current_line_number == target_line:
                        result = line_text.strip()
                        break  # stop reading file once we get our line

            memory[int(line[2], 2)] = result

        elif line[0] == "00010101": #writing to memory
            whatToWrite=memory[int(line[1], 2)]
            where = int(line[2],2)
            with open("memory.bhm", "r") as file:
                file_contents = file.read().splitlines()

            file_contents[where] = whatToWrite

            with open("memory.bhm", "w") as file:
                file.write("\n".join(file_contents) + "\n")
        
        elif line[0] == "00001111":
            # fetch command token from memory (could be str/int/char) and normalize to 8-bit binary string
            raw_cmd = memory[int(line[1], 2)]
            if isinstance(raw_cmd, str) and all(c in '01' for c in raw_cmd) and len(raw_cmd) == 8:
                cmd_bin = raw_cmd
            else:
                # try parse as binary-string, then as int, then as single-char fallback
                try:
                    cmd_bin = format(int(str(raw_cmd), 2), '08b')
                except Exception:
                    try:
                        cmd_bin = format(int(raw_cmd), '08b')
                    except Exception:
                        cmd_bin = format(ord(str(raw_cmd)[0]), '08b')

            # collect and normalize args
            arg_bins = []
            for a in line[2:]:
                val = memory[int(a, 2)]
                if isinstance(val, str) and all(c in '01' for c in val) and len(val) == 8:
                    arg_bins.append(val)
                else:
                    try:
                        arg_bins.append(format(int(str(val), 2), '08b'))
                    except Exception:
                        try:
                            arg_bins.append(format(int(val), '08b'))
                        except Exception:
                            arg_bins.append(format(ord(str(val)[0]), '08b'))

            command_line = " ".join([cmd_bin] + arg_bins)

            # debug help (optional) — shows exactly what you're about to execute
            print("CALL ->", command_line)

            # run the constructed single-line command in isolation
            saved_current = currentLine
            currentLine = 0               # ensure nested run starts at its own beginning
            interprit(command_line, o44=True)
            currentLine = saved_current   # restore outer execution point


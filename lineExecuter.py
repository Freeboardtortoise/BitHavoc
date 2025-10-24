import time
import globalVar as gv
import sys
import threading
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
def get_value(bit):
    if bit[0] == "1": #is memory
        return int(gv.memory[int(bit[1:], 2)])
    else:
        return int(bit[1:], 2)
def to_bin(thing):
        return "0"+(bin(thing)[2:])


class executor:
    def init():
        pass

    def threadIT(self,  startLine, endLine, code):
        newCode = code[startLine:endLine]
        threading.Thread(target=self.newThread, args=(newCode, )).start()

    def newThread(self,  code):
        current_line = 0
        while current_line < len(code.splitlines()):
            line = code[current_line]
            self.execute_line(line)
            current_line += 1
    def execute_line(self,  line):
        if len(" ".join(line)) < 7:
            gv.currentLine += 1
            return False
        if line[0] == "00000001":
            if line[2][0] == "1":
                line[2] = line[2][1:]
            else:
                print(line)
                print("what do you want me to do with this mov thing?\nI cant mov a number into a number?")
            gv.memory[int(line[1],2)] = get_value(line[2])

        elif line[0] == "00000010":
            gv.memory[get_value(line[1])] = to_bin(ord(read_char()))
        elif line[0] == "00000011":
            address = get_value(line[1])
            if len(line) >= 3:
                arg = line[2]
            else:
                arg = "00000001"
            if arg == "00000011":
                print(to_bin(address))
            if arg == "00000010":
                print(address,end='', flush=True)
            if arg == "00000001":
                print(chr(address), end='', flush=True)

        # mathamatical operations
        elif line[0] == "00010100":
            gv.memory[get_value(line[1])] = to_bin(
                get_value(line[2]) + get_value(line[3]))
        elif line[0] == "00011100":
            gv.memory[get_value(line[1])] = to_bin(
                get_value(line[2]) * get_value(line[3]))
        elif line[0] == "00011000":
            gv.memory[get_value(line[1])] = to_bin(
                get_value(line[2]) - get_value(line[3]))
        elif line[0] == "00011010":
            gv.memory[get_value(line[1])] = to_bin(
                get_value(line[2]) / get_value(line[3]))
        gv.currentLine += 1

        if line[0][0] == "1":  # if statements
            if line[0] == "00100001":
                if get_value(line[1]) == get_value(line[2]):
                    gv.currentLine = get_value(line[3])
            elif line[0] == "00100010":
                if get_value(line[1]) >= get_value(line[2]):
                    gv.currentLine = get_value(line[3])
            elif line[0] == "00100011":
                if get_value(line[1]) <= get_value(line[2]):
                    gv.currentLine = get_value(line[3])
            elif line[0] == "00100110":
                if get_value(line[1]) > get_value(line[2]):
                    gv.currentLine = get_value(line[3])
            elif line[0] == "00100111": # less than
                if get_value(line[1]) < get_value(line[2]):
                    gv.currentLine = get_value(line[3])
            elif line[0] == "00100101":
                if get_value(line[1]) != get_value(line[2]):
                    gv.currentLine = get_value(line[3])
        elif line[0] == "00001010":  # reading a specific line from file
            target_line = get_value(line[1])
            result = 0  # default value if line not found

            with open("gv.memory.bhm", "r") as file:
                for current_line_number, line_text in enumerate(file):
                    if current_line_number == target_line:
                        result = line_text.strip()
                        break  # stop reading file once we get our line

            gv.memory[int(line[2], 2)] = result

        elif line[0] == "00010101":  # writing to gv.memory
            whatToWrite = to_bin(int(line[1]))
            where = get_value(line[2])
            with open("memory.bhm", "r") as file:
                file_contents = file.read().splitlines()

            file_contents[where] = whatToWrite

            with open("gv.memory.bhm", "w") as file:
                file.write("\n".join(file_contents) + "\n")

        elif line[0] == "00001111":
            # fetch command token from gv.memory (could be str/int/char) and normalize to 8-bit binary string
            raw_cmd = get_value(line[1])
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
                val = gv.memory[int(a, 2)]
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

            # run the constructed single-line command in isolation
            saved_current = gv.currentLine
            gv.currentLine = 0               # ensure nested run starts at its own beginning
            self.interprit(command_line, o44=True)
            gv.currentLine = saved_current   # restore outer execution point
        elif line[0] == "01000000": # goto
            gv.currentLine = get_value(line[1])
        elif line[0] == "01011111":  # threading
            startLine = get_value(line[0])
            endLine = get_value(line[1])
            self.startTime = get_value(line[2])
            self.threadIT(startLine, endLine, gv.code)
        elif line[0] == "01001010":
            time.sleep(get_value(line[1])/100)
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

class executor:
    def init():
        pass
        
    def threadIT(self,  startLine, endLine, code):
        newCode = code[startLine:endLine]
        threading.Thread(target=self.newThread, args=(newCode, )).start()

    def newThread(self,  code):
        current_line=0
        while current_line < len(code.splitlines()):
            line = code[current_line]
            self.execute_line(line)
            current_line+=1
    def execute_line(self,  line):
        if len(" ".join(line)) < 7:
            gv.currentLine+=1
            return False
        line = line.split(" ")
        if line[0] == "00000001":
            gv.memory[int(line[1], 2)] = gv.memory[int(line[2], 2)]
        elif line[0] == "00000010":
            gv.memory[int(line[1], 2)] = "0"+bin(ord(read_char()))[2:]
        elif line[0] == "00000011":
            address = int(line[1], 2)
            print(chr(int(gv.memory[address],2)), end='', flush=True)
        elif line[0] == "00000100":
            gv.memory[int(line[1],2)] = line[2]

        # mathamatical operations
        elif line[0] == "00010100":
            gv.memory[int(line[1],2)] = bin(int(gv.memory[int(line[2],2)],2) + int(gv.memory[int(line[3],2)],2))[2:]
        elif line[0] == "00011100":
            gv.memory[int(line[1],2)] = bin(int(gv.memory[int(line[2],2)],2) * int(gv.memory[int(line[3],2)],2))[2:]
        elif line[0] == "00011000":
            gv.memory[int(line[1],2)] = bin(int(gv.memory[int(line[2],2)],2) - int(gv.memory[int(line[3],2)],2))[2:]
        elif line[0] == "00011010":
            gv.memory[int(line[1],2)] = bin(int(gv.memory[int(line[2],2)],2) / int(gv.memory[int(line[3],2)],2))[2:]
        gv.currentLine+=1

        if line[0][0] == "1": #if statements
            if line[0] == "00100001":
                if gv.memory[int(line[1], 2)] == gv.memory[int(line[2], 2)]:
                    gv.currentLine=int(line[3], 2)
                    print(f"goto {int(line[3], 2)}")
            elif line[0] == "00100010":
                if gv.memory[int(line[1],2)] >= gv.memory[int(line[2],2)]:
                    gv.currentLine=int(line[3], 2)
            elif line[0] == "00100011":
                if gv.memory[int(line[1],2)] <= gv.memory[int(line[2],2)]:
                    gv.currentLine=int(line[3], 2)
            elif line[0] == "00100110":
                if gv.memory[int(line[1],2)] > gv.memory[int(line[2],2)]:
                    gv.currentLine=int(line[3], 2)
            elif line[0] == "00100111":
                if gv.memory[int(line[1],2)] < gv.memory[int(line[2],2)]:
                    gv.currentLine=int(line[3], 2)
            elif line[0] == "00100101":
                if gv.memory[int(line[1],2)] != gv.memory[int(line[2],2)]:
                    gv.currentLine=int(line[3], 2)
        elif line[0] == "00001010":  # reading a specific line from file
            target_line = int(gv.memory[int(line[1], 2)], 2)
            result = '00000000'  # default value if line not found

            with open("memory.bhm", "r") as file:
                for current_line_number, line_text in enumerate(file):
                    if current_line_number == target_line:
                        result = line_text.strip()
                        break  # stop reading file once we get our line

            gv.memory[int(line[2], 2)] = result

        elif line[0] == "00010101": #writing to gv.memory
            whatToWrite=gv.memory[int(line[1], 2)]
            where = int(line[2],2)
            with open("memory.bhm", "r") as file:
                file_contents = file.read().splitlines()

            file_contents[where] = whatToWrite

            with open("gv.memory.bhm", "w") as file:
                file.write("\n".join(file_contents) + "\n")
        
        elif line[0] == "00001111":
            # fetch command token from gv.memory (could be str/int/char) and normalize to 8-bit binary string
            raw_cmd = gv.memory[int(line[1], 2)]
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
        elif line[0] == "01000000":
            gv.currentLine = int(line[1], 2)
        elif line[0] == "01011111": #threading
            startLine=int(line[0],2)
            endLine=int(line[1],2)
            self.startTime=int(line[2],2)
            self.threadIT(startLine,endLine,gv.code)
        elif line[0] == "01001010":
            time.sleep(int(line[1], 2))

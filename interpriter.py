import time
memory = [0] * 10000000
functions = []
currentLine = 0
def interprit(code, arg=None):
    global functions, memory, currentLine
    print("setting memory")
    if arg is not None:
        memory[int("100000",2)] = arg
    newCode=code.split("\n")
    while currentLine < len(newCode):
        time.sleep(0.01)
        line = newCode[currentLine]
        line = line.split(" ")
        print(line)

        if line[0] == "000001":
            memory[int(line[1], 2)] = memory[int(line[2], 2)]
        elif line[0] == "000010":
            memory[int(line[1], 2)] = ord(input()[0])
        elif line[0] == "000011":
            address = int(line[1], 2)
            print(chr(memory[address]), end='')
        elif line[0] == "000101":
            memory[int(line[1],2)] = int(line[2], 2)

        # mathamatical operations
        elif line[0] == "010100":
            memory[int(line[1],2)] = memory[int(line[2],2)] + memory[int(line[3],2)]
        elif line[0] == "011100":
            memory[int(line[1],2)] = memory[int(line[2],2)] * memory[int(line[3],2)]
        elif line[0] == "011000":
            memory[int(line[1],2)] = memory[int(line[2],2)] - memory[int(line[3],2)]
        elif line[0] == "011000":
            memory[int(line[1],2)] = memory[int(line[2],2)] / memory[int(line[3],2)]
        elif line[0] == "110001":
            functions.append([line[1],line[2:]])
        currentLine+=1

        if line[0][0] == "1": #if statements
            print("if")
            if line[0] == "100001":
                print("==")
                if memory[int(line[1], 2)] == memory[int(line[2], 2)]:
                    currentLine=int(line[3], 2)
                    print(f"goto {int(line[3], 2)}")
            elif line[0] == "100010":
                if memory[int(line[1],2)] >= memory[int(lint[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100011":
                if memory[int(line[1],2)] <= memory[int(lint[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100110":
                if memory[int(line[1],2)] > memory[int(lint[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100111":
                if memory[int(line[1],2)] < memory[int(lint[2],2)]:
                    currentLine=int(line[3], 2)
            elif line[0] == "100101":
                if memory[int(line[1],2)] != memory[int(lint[2],2)]:
                    currentLine=int(line[3], 2)
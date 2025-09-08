memory = [0] * 1000000
functions = []
def interprit(code, arg=None):
    global functions, memory
    print("setting memory")
    if arg is not None:
        memory[int("100000",2)] = arg
    for line in code.split("\n"):
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
        elif line[0] == "000100":
            memory[int(line[1],2)] = memory[int(line[2],2)] + memory[int(line[3],2)]
        elif line[0] == "001100":
            memory[int(line[1],2)] = memory[int(line[2],2)] * memory[int(line[3],2)]
        elif line[0] == "001000":
            memory[int(line[1],2)] = memory[int(line[2],2)] - memory[int(line[3],2)]
        elif line[0] == "001010":
            memory[int(line[1],2)] = memory[int(line[2],2)] / memory[int(line[3],2)]
        elif line[0] == "100001":
            functions.append([line[1],line[2:]])

	# functions
        elif line[0].startswith("1"):
            for function in functions:
                if function[0] == line[0]:
                    interprit(" ".join(function[1]) + "\n", arg)
        print(memory[0:10])

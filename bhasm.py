ref_table = {"mov": "00000001", 
             "output": "00000011",
             "bin": "00000011",
             "int": "00000010",
             "asci": "00000001",
             "if_eq": "00100001",
             "ifgteq": "00100010",
             "iflteq": "00100011",
             "ifgt": "00100110",
             "iflt": "00100111",
             "ifneq": "00100101",
             "exec": "00001111",
             "wait": "01001010",
             "thread": "01011111",
             "read": "00001010",
             "write": "00010101",
             "input": "00000010",
             "asci": "00000010",
             "mem": "1",
             "val": "0"
             }

def convert(code):
    output = ""
    cline = ""
    for line in code.split("\n"):
        line = line.split(" ")
        cline = ""
        for num, thing in enumerate(line):
            if thing == "mem":
                cline = cline + "1"
            elif thing == "val":
                cline = cline + "0"
            else:
                if thing in ref_table:
                    whatToWrite = ref_table[thing]
                else:
                    whatToWrite = thing
                cline = cline + whatToWrite + " "
        whatToWrite = ""
        output = output + cline + "\n"
    return output

def main():
    import sys
    file = sys.argv[1]
    output = sys.argv[2]
    code = convert(open(file, "r").read())
    with open(output, "w") as file:
        file.write(code)

main()
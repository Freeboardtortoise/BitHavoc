print("wellcome to bin Bash asm language... the better way to code in binbash")
import os
import sys

if sys.argv[1] == "compile":
    print("compiling to bitHavoc")
    file = sys.argv[2]
    newFile = ""
    with open(file,"w") as f:
        contents = f.read()
    for line in contents.split("\n"):
        splitLine = line.strip().split(" ")
        if splitLine[0] == "sv": #set value
            newFile = newFile + f"00000100 {splitLine[1]} {splitLine[2]}\n"
        elif splitLine[0] == "mov":
            newFile = newFile + f"00000001 {splitLine[1]} {splitLine[2]}\n"
        elif splitLine[0] == "stdout":
            newFile = newFile + f"00000011 {splitLine[1]}\n"
        elif splitLine[0] == "stdin":
            newFile = newFile + f"00000010 {splitLine[1]}\n"
        elif splitLine[0] == "exec":

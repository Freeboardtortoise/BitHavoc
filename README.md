# BIT HAVOC

## What is bit havoc

bit havoc is a binary style language for writing little toy OS's.

## The language

The language consists of 4 charactors
1,0, ,\n
in the BitHavocEditor those are the only charactors you can type and the rest will be 1 if it is on the left side of the keyboard and 0 if it is on the right.

## How to use bitHavoc

clone the Repo

```
git clone https://github.com/Freeboardtortoise/BitHavoc.git
cd BitHavoc
```

Install python

```
--- arch based OS ---
sudo pacman -S python3
--- ubuntu based OS ---
sudo apt install python3
--- windows ---
figure it out
```

start editing a .bh file with the bhEditor

```
python3 editor.py main.bh
```

create persistant storage (if needed)

```
python3 main.py create-persistant-storage
```

run the bitHavoc file

```
python3 main.py run main.bh
```

## what is the bitHavocEditor

The bitHavoc editor is an editor that prioritises speed and you can only type 1 0 space or enter

## commands and controls for the BH editor

| Command | what does it do                                                                                          |
| ------- | -------------------------------------------------------------------------------------------------------- |
| q       | quits the editor                                                                                         |
| s       | saves the file (if there is no file you opened or not saved to anything eg. new file it will prompt you) |
| l       | loads a file (will prompt you for a file name or path)                                                   |

## bitHavoc op Codes

| Op code  | function                          |
| -------- | --------------------------------- |
| 00000001 | move something somewhere          |
| 00000010 | read from user 1 bit into [1]     |
| 00000011 | write memory adress [1] to screen |

mov args
| arg space | arg option | what it does |
|-----------|------------|--------------|
| 3 | 00000001 | memory[1] to memory[2] |
| 3 | 00000010 | memory[1] to var[2] |

printing args
| arg place | arg value | what it does |
|-----------|-----------|--------------|
| 2 | 00000010 | print the number value |
| 2 | 00000001 | print the asci value |
| 2 | 00000011 | print the raw bin value|

If statements
|Opt Code|function|
|--------|--------|
| 00100001 |if [0] == [1] goto line [2] |
| 00100010 |if [0] >= [1] goto line [2] |
| 00100011 |if [0] <= [1] goto line [2] |
| 00100110 |if [0] > [1] goto line [2] |
| 00100111 |if [0] < [1] goto line [2] |
| 00100101 |if [0] != [1] goto line [2] |

running from memory
| Opt Code | function |
|-----|-----|
| 00001111 | run from memory [1] with args [memory[line[2]:]] |

persistant storage
| Opt Code | function |
| 00001010 | load from persistant memory from [1] to [2] in memory |
| 00010101 | write to persistant memory from memory at [1] to persistant at [2] |

Threading
| Opt Code | function |
| 01011111 | threading start new thread at line [0] and end at line [1], start at time [2] and call it [3]

Time
| Opt Code | function |
| ------------- | ----------- |
| 01001010 | waits [1] secconds |

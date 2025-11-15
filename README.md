# BIT HAVOC

## What is bit havoc

bit havoc is a binary style eccentric programming language for writing little toy OS's.

## The language

The language consists of 4 charactors
1,0, ,\n

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

create persistant storage (if needed)

```
python3 main.py create-persistant-storage
```

run the bitHavoc file

```
python3 main.py run main.bh
```

## bitHavoc op Codes

| Op code  | function                          |
| -------- | --------------------------------- |
| 00000001 | set [1] to [2]   |
| 00000010 | read from user 1 bit into [1]     |
| 00000011 | write [1] to screen |

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
|----------|----------|
| 00001010 | load from persistant memory from [1] to [2] in memory |
| 00010101 | write to persistant memory from memory at [1] to persistant at [2] |

Threading
| Opt Code | function |
| 01011111 | threading start new thread at line [0] and end at line [1], start at time [2] and call it [3]

Time
| Opt Code | function |
| ------------- | ----------- |
| 01001010 | waits [1] secconds |

*General memory and things*

if the value starts with 0 then it is a memory address
if the value starts with 1 then it is a hard coded value

import threading
import time
from lineExecuter import execute_line

def threadIT(startLine, endLine, code):
    newCode = code[startLine:endLine]
    threading.thread(newThread, args=(newCode, )).start()

def newThread(code):
    current_line=0
    while currentLine < len(code.splitlines()):
        line = newCode[currentLine]
        execute_line(line)
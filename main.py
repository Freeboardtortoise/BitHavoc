import time
import interpriter

print("wellcome to binbash")
print("the language that like binary")

import sys
file=sys.argv[1]
with open(file, "r") as file:
    file = file.read()
interpriter.interprit(file)

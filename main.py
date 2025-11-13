import sys
import interpriter  # Assuming this is your safe custom module
import globalVar as gv

def parse_flags():
    args = sys.argv
    args = args[3:]
    for arg in args:
        if arg == "-h":
            print("Usage: python script.py <command> <arg>")
            print("Commands:")
            print("  run <filename> <flags>")
            print("  create-persistent-storage <size>")
            return
        elif arg == "-d":
            gv.debug = True
        else:
            if arg.split("=")[0] == "-t" or "--run-tests":
                # running unit tests
                gv.testing = True
            if arg.split("=")[0] == "s" or "--set":
                # set some memory to a value
                print(arg.split("=")[1].split(":")[0])
                gv.memory[int(arg.split("=")[1].split(":")[0],2)] = arg.split("=")[1].split(":")[1]
                print("done")



def main():
    print("Welcome to binbash")
    print("The language that likes binary")

    # Check for minimum required args
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> <arg>")
        print("Commands:")
        print("  run <filename> <flags>")
        print("  create-persistent-storage <size>")
        return 1

    command = sys.argv[1]
    if len(sys.argv) == 2:
        print("noarg")
    else:
        arg = sys.argv[2]
    flags = sys.argv[3:]

    if command == "run":
        if len(sys.argv) == 2:
            print ("flags for run:")
            print ("""
            	-d     --debug          the flag to enable debug mode
            	-v     --verbose        The flag used to enable vebose mode
            	-s     --set            Change the memory value at a location
            	-t     --run-tests      Run tests on your code
            usage: command run <file> -dv --run-tests="tests/*"
            	""")
            return 1
        else:
            parse_flags()
#        try:
        # Basic validation to avoid dangerous paths, can add more checks
        if ".." in arg or arg.startswith("/"):
            print("Invalid filename")
            return
        with open(arg, "r") as f:
            code = f.read()

        interpriter.interprit(code)

#        except FileNotFoundError:
#          print(f"File not found: {arg}")
#        except IOError as e:
#           print(f"Error reading file: {e}")
#        except Exception as e:
#            print(f"An error occurred while interpreting the file: {e}")

    elif command == "create-persistent-storage":
        try:
            size = int(arg)
            if size <= 0:
                print("Size must be a positive integer")
                return

            interpriter.createMemoryFile(size)
        except ValueError:
            print("Invalid size: must be an integer")
        except Exception as e:
            print(f"An error occurred while creating persistent storage: {e}")

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

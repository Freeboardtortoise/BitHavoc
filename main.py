import sys
import interpriter  # Assuming this is your safe custom module

def main():
    print("Welcome to binbash")
    print("The language that likes binary")

    # Check for minimum required args
    if len(sys.argv) < 3:
        print("Usage: python script.py <command> <arg>")
        print("Commands:")
        print("  run <filename>")
        print("  create-persistent-storage <size>")
        return

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "run":
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

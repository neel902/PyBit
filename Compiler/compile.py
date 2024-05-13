import prnExtra
from prnExtra import Flags
import time

import sys

#prnExtra.clearConsole()
#prnExtra.prnExtra("Compiling code...", Flags.ConsoleFonts.BOLD)
#prnExtra.prnExtra("Tokenising - 5%", Flags.ConsoleColours.GREEN, Flags.ConsoleFonts.BOLD)

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage (With Compiler as current directory): python3 compile.py <file_name>")
    else:
        file_name = sys.argv[1]
        print("File Name: ", file_name)
        

if __name__ == "__main__":
    main()
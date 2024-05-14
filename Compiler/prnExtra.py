from functools import partial

class Flags:
    class ConsoleColours:
        BLACK = 30
        RED = 31
        GREEN = 32
        YELLOW = 33
        BLUE = 34
        MAGENTA = 35
        CYAN = 36
        WHITE = 37
        BRIGHT_BLACK = 90
        BRIGHT_RED = 91
        BRIGHT_GREEN = 92
        BRIGHT_YELLOW = 93
        BRIGHT_BLUE = 94
        BRIGHT_MAGENTA = 95
        BRIGHT_CYAN = 96
        BRIGHT_WHITE = 97

        RESET = 49
    class ConsoleFonts:
        BOLD = 1
        NO_BOLD = 21

        UNDER = 4
        NO_UNDER = 24

def prnExtra(text, *flags):
    print(formatText(text, *flags))

def formatText(text, *flags):
    ftext = f"{text}\033[0m"
    form = "\033["
    for flag in flags:
        form += str(flag) + ";"
    form = form[:-1] + "m"
    ftext = form + ftext
    return ftext

def clearConsole():
    print("\n" * 50)

if __name__ == "__main__":
    for i in range(30, 37 + 1):
        print("\033[%dm%d\t\t\033[%dm%d" % (i, i, i + 60, i + 60))

    print("\033[39m\\033[49m                 - Reset color")
    print("\\033[2K                          - Clear Line")
    print("\\033[<L>;<C>H or \\033[<L>;<C>f  - Put the cursor at line L and column C.")
    print("\\033[<N>A                        - Move the cursor up N lines")
    print("\\033[<N>B                        - Move the cursor down N lines")
    print("\\033[<N>C                        - Move the cursor forward N columns")
    print("\\033[<N>D                        - Move the cursor backward N columns\n")
    print("\\033[2J                          - Clear the screen, move to (0,0)")
    print("\\033[K                           - Erase to end of line")
    print("\\033[s                           - Save cursor position")
    print("\\033[u                           - Restore cursor position\n")
    print("\\033[4m                          - Underline on")
    print("\\033[24m                         - Underline off\n")
    print("\\033[1m                          - Bold on")
    print("\\033[21m                         - Bold off")
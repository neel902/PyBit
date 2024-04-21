import main as prm
import sys

def main() -> None:
    try:
        arg1 = sys.argv[1]
    except:
        sys.exit("Expected 1 argument")
    with open(arg1) as f:
        prm.run(f"\n{f.read()}\n")
    input()

if __name__ == "__main__":
    main()
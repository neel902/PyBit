import os
import sys
import json

path = input(".piso Path: ")

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
ROM_path = f"{dir_path}\\ROM.pb8"
files_path = f"{dir_path}\\disk.json"

files = {}
rom = ""

try:
    f = open(path, "r")
    exec(f.read(), {"files" : files, "rom" : rom, "ROM" : rom})
except Exception as e:
    sys.exit(e)
finally:
    f.close()

with open(files_path, "w") as f:
    f.write(json.dumps(files))

with open(ROM_path, "w") as f:
    f.write(rom)
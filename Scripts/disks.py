import json
import os
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
def getFile(address):
    with open(f"{dir_path}\\disk.json", "r") as f:
        jStr = (f.read())
    j = json.loads(jStr)
    return j[address] if address in j.keys() else "404ERRORREGISTRYDOESNOTEXIST"
def setFile(address, value):
    if not value == "404ERRORREGISTRYDOESNOTEXIST":
        with open(f"{dir_path}\\disk.json", "r") as f:
            jStr = (f.read())
        j = json.loads(jStr)
        j[address] = value
        with open(f"{dir_path}\\disk.json", "w") as f:
            f.write(json.dumps(j))
def list():
    l = []
    with open(f"{dir_path}\\disk.json", "r") as f:
        jStr = (f.read())
    j = json.loads(jStr)
    for i in j.keys():
        l.append(i)
    return l
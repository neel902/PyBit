data = {
    "a":"hi",
    "b":{
        "data":"ducks"
    }
}


msg = "$%a$ $%b.data$ hello"


result = ""
spal = msg.split("$")
for i in spal:
    if i != "":
        if i[0] == "%":
            if "." in i:
                ssp = i[1:].split(".")
                current = data
                for i2 in ssp:
                    current = current[i2]
                result += current
            else:
                result += data[i[1:]]
        else:
            result += i

print(result)
from PIL import Image
import win32clipboard

def setClipboard(text : str) -> None:
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

def n255to8(num):
    num = int(num/2)
    num = bin(num).replace("0b","")
    numBin = "0" * (7 - len(num)) + num
    return numBin

imgPath = input("Path to image: ")

# Open an image file

image = Image.open(imgPath)



# Convert the image to RGB mode if it's not already in RGB
image = image.convert('RGB')

# Get the RGB values as a list of tuples
rgb_list = list(image.getdata())

flat_rgb_list = ""

# If you want to further convert the list to a flat list of RGB values
last_rgb = (-1,-1,-1)
count = 0
for i in rgb_list:
    if i == last_rgb:
        count += 1
    else:
        if last_rgb != (-1, -1, -1):
            flat_rgb_list += f"{count}*{n255to8(last_rgb[0])},{n255to8(last_rgb[1])},{n255to8(last_rgb[2])}-"
        count = 1
        last_rgb  = i

flat_rgb_list += f"{count}*{n255to8(last_rgb[0])},{n255to8(last_rgb[1])},{n255to8(last_rgb[2])}-"
flat_rgb_list = f"{str(image.size[1])}-{str(image.size[0])}-{flat_rgb_list[:-1]}"

print(flat_rgb_list)
setClipboard(flat_rgb_list)

image.close()
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
    numBin = "0" * (8 - len(num)) + num
    return numBin

imgPath = input("Path to image: ")

# Open an image file

image = Image.open(imgPath)



# Convert the image to RGB mode if it's not already in RGB
image = image.convert('RGB')

# Get the RGB values as a list of tuples
rgb_list = list(image.getdata())

# If you want to further convert the list to a flat list of RGB values
flat_rgb_list = "-".join([n255to8(rgb) for pixel in rgb_list for rgb in pixel])

flat_rgb_list = f"{str(image.size[0])}-{str(image.size[1])}-{flat_rgb_list}"

print(flat_rgb_list)
setClipboard(flat_rgb_list)

image.close()
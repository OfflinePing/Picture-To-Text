import PIL.Image
import pyperclip
import pystray
from PIL import ImageGrab
import pytesseract
from pynput.mouse import Controller, Listener


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
config = ('-l eng --oem 1 --psm 3')
mouse = Controller()
icn = PIL.Image.open("icon.png")


def get_screen(arg1, arg2):
    image = ImageGrab.grab(bbox=(arg1[0], arg1[1], arg2[0], arg2[1]), all_screens=True)
    return image


def on_click(x, y, button, pressed):
    global first
    global second
    if pressed:
        first = x, y
    else:
        second = x, y
    if not pressed:
        return False


def on_clicked(icon, item):
    if str(item) == "Grab Text":
        with Listener(on_click=on_click) as listener:
            listener.join()
            img = get_screen(first, second)
            text = pytesseract.image_to_string(img, config=config)
            pyperclip.copy(text)
    elif str(item) == "Exit":
        icon.stop()

icon = pystray.Icon("Neural", icn, menu=pystray.Menu(pystray.MenuItem("Grab Text", on_clicked), pystray.MenuItem("Exit", on_clicked)))

if __name__ == "__main__":
    icon.run()

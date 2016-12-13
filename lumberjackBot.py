import pyautogui
import time
from ctypes import windll
import threading 


class lumberjackBot():

    __author__ = "EnriqueMoran"

    def __init__(self, playX, playY, treeX, treeY):
        self.playX = playX
        self.playY = playY
        self.treeX = treeX
        self.treeY = treeY
        # Those attributes has been placed here in order to save calcs: 
        self.pixelL = (0,0,0)   # Left side branch color
        self.pixelR = (0,0,0)   # Right side branch color
        self.lX = treeX - 30    # Left side branch X location
        self.rX = treeX + 30    # Right side branch X location
        self.y = treeY - 130    # Both side branch Y location


    def move(self, direction):
        if direction == "left":
            pyautogui.typewrite(['left'])
            pyautogui.typewrite(['left'])
        elif direction == "right":
            pyautogui.typewrite(['right'])
            pyautogui.typewrite(['right'])

    def get_color(self, rgb):
        r = rgb & 0xff
        g = (rgb >> 8) & 0xff
        b = (rgb >> 16) & 0xff
        return r,g,b

    def get_pixel(self, x, y, side):    # Modify class atribute
        screen = windll.user32.GetDC(0)
        rgb = windll.gdi32.GetPixel(screen, x, y)
        if side == 'L':
            self.pixelL = self.get_color(rgb)
        elif side == 'R':
            self.pixelR = self.get_color(rgb)

    def play(self):
        self.move("right")
        while True:
            if self.pixelL == (161, 116, 56): # or self.pixelL == (153, 110, 54):
                self.move("right")
            elif self.pixelR == (161, 116, 56): # or self.pixelR == (153, 110, 54):
                self.move("left")

    def pixelThreadL(self):
        while True:
            self.get_pixel(self.lX, self.y, 'L')

    def pixelThreadR(self):
        while True:
            self.get_pixel(self.rX, self.y, 'R')


if __name__ == "__main__":
    playX, playY = pyautogui.locateCenterOnScreen('playButton.png')
    pyautogui.moveTo(playX, playY)
    pyautogui.click()   # Start the game by pressing play button
    time.sleep(0.5)     # Wait for screen refresh
    treeX, treeY = pyautogui.locateCenterOnScreen('tree.png') # Recognize tree position
    time.sleep(0.3)
    print("Im playing... To stop me click on IDLE and press CTRL+F6.")
    lumberjack = lumberjackBot(playX, playY, treeX, treeY)
    t1 = threading.Thread(target = lumberjack.pixelThreadL, args = ())
    t2 = threading.Thread(target = lumberjack.pixelThreadR, args = ())
    t1.start()
    t2.start()
    lumberjack.play()   # Game start

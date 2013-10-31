# ...An attempt to control my Nexus 4 with a smashed touch screen.
# by Pengyu CHEN (cpy.prefers.you[at]gmail.com)
# COPYLEFT, ALL WRONGS RESERVED.

# For Python 3.0+ only now.

import io
import subprocess
import threading
import tkinter

from PIL import Image
from PIL import ImageTk

def get_screen_image():
    """ Notice: throws exception! """
    p0 = subprocess.Popen(['adb', 'shell', 'screencap', '-p'],
        stdout=subprocess.PIPE)
    p1 = subprocess.Popen(['sed', 's/\r$//'], stdin=p0.stdout,
        stdout=subprocess.PIPE)
    p0.stdout.close()
    scr_png_data = p1.communicate()[0]
    scr_img = Image.open(io.BytesIO(scr_png_data))
    return scr_img
    
class Smashed_UI(object):
    
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.resizable(0,0)

        self.img_label = tkinter.Label(self.root, image=None)
        self.img_label.bind('<ButtonPress-1>', self.button_press)
        self.img_label.bind('<ButtonRelease-1>', self.button_release)
        self.img_label.bind('<B1-Motion>', self.button_motion)
        self.img_label.bind('<Key>', self.key_pressed)
        self.img_label.pack()
        self.img_label.focus_set()

        return

    def __fini__(self):
        return

    oldpos = None
    is_swipe = False

    def button_press(self, event):
        self.oldpos = (event.x, event.y)
        return

    def button_release(self, event):
        if not self.is_swipe:
            subprocess.call('adb shell input touchscreen tap %d %d'
                %(event.x, event.y), shell=True)
            print('adb shell input touchscreen tap %d %d'%(event.x, event.y))
        self.oldpos = None
        self.is_swipe = False
        return

    def button_motion(self, event):
        if self.oldpos:
            subprocess.call('adb shell input touchscreen swipe %d %d %d %d'
                %(self.oldpos[0], self.oldpos[1], event.x, event.y), shell=True)
            print('adb shell input touchscreen swipe %d %d %d %d'
                %(self.oldpos[0], self.oldpos[1], event.x, event.y))
            self.is_swipe = True
            self.oldpos = (event.x, event.y)
        return

    def key_pressed(self, event):
        if len(event.char) > 1: # special key
            return
        keycode = 0 # unknown
        key = event.char[0]
        # Hardcoded. See:
        # http://developer.android.com/reference/android/view/KeyEvent.html
        if key >= '0' and key <= '9':
            keycode = ord(key) - ord('0') + 7
        elif key == '*':
            keycode = 17
        elif key == '#':
            keycode = 18
        elif key >= 'A' and key <= 'Z':
            keycode = ord(key) - ord('A') + 29
        elif key >= 'a' and key <= 'z':
            keycode = ord(key) - ord('a') + 29
        elif key == ',':
            keycode = 55
        elif key == '.':
            keycode = 56
        elif key == '\t':
            keycode = 61
        elif key == ' ':
            keycode = 62
        elif key == '\n':
            keycode = 66
        elif key == '\b':
            keycode = 67
        elif key == '`':
            keycode = 68
        elif key == '-':
            keycode = 69
        elif key == '=':
            keycode = 70
        elif key == '[':
            keycode = 71
        elif key == ']':
            keycode = 72
        elif key == '\\':
            keycode = 73
        elif key == ';':
            keycode = 74
        elif key == '\'':
            keycode = 75
        elif key == '/':
            keycode = 76
        elif key == '@':
            keycode = 77
        elif key == '+':
            keycode = 81
        else:
            keycode = 0

        if keycode != 0:
            subprocess.call('adb shell input keyevent %d'%keycode, shell=True)
            print('adb shell input keyevent %d'%keycode)
        return

    def refresh_(self):
        try:
            scr_img = get_screen_image()
            self.scr_img_tk = ImageTk.PhotoImage(scr_img)
            self.img_label['image'] = self.scr_img_tk
            self.root.update_idletasks()
        except:
            pass
        self.root.after(0, self.refresh)
        return

    def refresh(self):
        self.scr_img_tk = self.scr_img_tk_new
        self.img_label['image'] = self.scr_img_tk
        self.root.update_idletasks()
        return
    
    def main_loop(self):
        self.root.mainloop()
        return

class Refresher(threading.Thread):
    
    def __init__(self, smashed_UI):
        super().__init__()
        self.smashed_UI = smashed_UI

    _post_stop = False

    def run(self):
        while not self._post_stop:
            try: 
                scr_img = get_screen_image()
                if self._post_stop:
                    break
                self.smashed_UI.scr_img_tk_new = ImageTk.PhotoImage(scr_img)
                self.smashed_UI.root.after(10, self.smashed_UI.refresh)
            except:
                pass
        return

    def post_stop(self):
        self._post_stop = True
        return


def main():
    UI = Smashed_UI()
    refresher = Refresher(UI)
    refresher.start()
    UI.main_loop()
    refresher.post_stop()
    refresher.join()
    return

if __name__ == '__main__':
    main()








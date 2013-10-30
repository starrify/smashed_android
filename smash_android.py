# ...An attempt to control my Nexus 4 with a smashed touch screen.
# by Pengyu CHEN (cpy.prefers.you[at]gmail.com)
# COPYLEFT, ALL WRONGS RESERVED.

# For Python 3.0+ only now.

import io
import subprocess
import tkinter

from PIL import Image
from PIL import ImageTk

def get_screen_image():
    p0 = subprocess.Popen(['adb', 'shell', 'screencap', '-p'],
        stdout=subprocess.PIPE)
    p1 = subprocess.Popen(['sed', 's/\r$//'], stdin=p0.stdout,
        stdout=subprocess.PIPE)
    p0.stdout.close()
    scr_png_data = p1.communicate()[0]
    scr_img = Image.open(io.BytesIO(scr_png_data))
    return scr_img

def callback(event):
    print('clicked %d %d' %(event.x, event.y))
    return
    
class smashed_UI(object):
    
    def __init__(self):
        scr_img = get_screen_image()
        self.scr_size = scr_img.size
        self.root = tkinter.Tk()
        self.root.geometry('%dx%d'%self.scr_size)
        self.root.resizable(0,0)

        self.img_label = tkinter.Label(self.root, image=None)
        self.img_label.bind('<Button-1>', (lambda event:
            subprocess.call('adb shell input touchscreen tap %d %d'
                %(event.x, event.y), shell=True)))
        self.img_label.pack()

        return

    def __fini__(self):
        return

    def refresh(self):
        try:
            scr_img = get_screen_image()
            self.scr_img_tk = ImageTk.PhotoImage(scr_img)
            self.img_label['image'] = self.scr_img_tk
            #self.root.update()
            self.root.update_idletasks()
            self.root.after(0, self.refresh)
        except:
            pass
        return
    
    def main_loop(self):
        self.root.mainloop()
        return


def main():
    UI = smashed_UI()
    UI.refresh()
    #while True:
    #    UI.refresh()
    UI.main_loop()

    print('done')

if __name__ == '__main__':
    main()








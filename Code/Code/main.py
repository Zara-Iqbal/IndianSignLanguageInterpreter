from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from PIL import Image
from Prediction import pred_main
from Reverse_Recognition import rr_main

#global variables
bg=None
selection=1

window2 = Tk()
f1 = Frame(window2)
f2 = Frame(window2)
f3 = Frame(window2)
f4 = Frame(window2)

def swap(frame):
    frame.tkraise()

for frame in (f1, f2, f3, f4):
    frame.place(x=0, y=0, width=400, height=400)
window2.geometry("400x400+420+170")
window2.resizable(False, False)
label3 = Label(f1, text="DASHBOARD", font=("arial", 20, "bold"), bg="#1A120A", fg="white",
               relief=RAISED)
label3.pack(side=TOP, fill=X)

label4 = Label(f2, text="                            Indian Sign Language Recognition System", font=("arial", 10, "bold"), bg="grey16",
               fg="white")
label4.pack(side=BOTTOM, fill=X)
statusbar = Label(f1, text="                         Created by Faraz Suhail and Hardik Govil and Zara Iqbal", font=("arial", 11, "bold"),
  bg="#1A120A", fg="white", relief=RAISED, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever
        self._is_running = False
        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)
                i += 1
                im.seek(i)
        except EOFError:
            pass
        self._last_index = len(self._frames) - 1
        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100
        self._callback_id = None
        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return
        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])
        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return
        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None
        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])
        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).grid(**kwargs)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()
        super(AnimatedGIF, self).place(**kwargs)

    def pack_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()
        super(AnimatedGIF, self).place_forget(**kwargs)

if __name__ == "__main__":
    l = AnimatedGIF(f1, "files/gif2.gif")
    l.pack()

label4 = Label(f3, text="             Indian Sign Language Recognition System", font=("arial", 10, "bold"), bg="grey16",
               fg="white")
label4.pack(side=BOTTOM, fill=X)

style = ttk.Style()
style.configure('TButton', font = ('arial', 12, 'bold'), background = 'black', foreground = 'black', borderwidth = '7')

btn2w2 = ttk.Button(f1, text="Recognise Sign", style = 'TButton', command=pred_main)
btn2w2.place(x=125, y=125, width=150, height=30)

btn3w2 = ttk.Button(f1, text="Speech to Sign", style = 'TButton', command=rr_main)
btn3w2.place(x=125, y=175, width=150, height=30)

def quit():
    window2.destroy()

btn9w2 = ttk.Button(f1, text="Exit", style = 'TButton', command=quit)
btn9w2.place(x=125, y=225, width=150, height=30)

f1.tkraise()
window2.mainloop()
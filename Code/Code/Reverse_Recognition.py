def rr_main():
    import speech_recognition as sr
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.animation import FuncAnimation
    import tkinter as tk
    import imageio
    from tkinter import messagebox


    def display(img,title="Original"):
        plt.imshow(img,cmap='gray'),plt.title(title)
        plt.axis('off')
        plt.show(block=False)
        plt.pause(0.7)
        plt.close

    path=('Reverse sign images//')
    voice=sr.Recognizer()
    text=[]
    with sr.Microphone() as source:
        messagebox.showinfo('Info','Speak Now')
        audio=voice.listen(source)
        try:
            text=voice.recognize_google(audio)
            messagebox.showinfo('Info', 'You said: '+str(text))
        except:
            messagebox.showerror("error","Your voice is not clear")

    if text:
        text.lower()
    try:
        for l in text:
            if l is not ' ':
                img=imageio.imread(path+str(l)+'.jpg')
                display(img,l)
    except:
        messagebox.showerror("error","There was an error reading the input")
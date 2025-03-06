import requests
import os
from PIL import Image, ImageTk
from pynput.mouse import Listener
import threading
import tkinter as tk
import pytesseract
import pyautogui
import threading
import time
from transformers import MarianMTModel, MarianTokenizer



pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
is_d = 1
model_name = "peterhsu/marian-finetuned-kde4-en-to-zh_TW"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)
x = ''
def calltrans(t): #en翻譯zh-tw
    global x
    encoded = tokenizer.encode(t, return_tensors='pt')
    translated = model.generate(encoded)
    translation = tokenizer.decode(translated[0], skip_special_tokens=True)
    x = translation
    w = root.winfo_width()
    h = root.winfo_height()
    u = ""
    i=0
    c = len(x)
    size = w*h/c
    size = size ** 0.3
    word = int(w/(size*2.4))
    print(size, word)
    while i < c :
        u += x[i:i+word]
        u += "\n"
        i += word

    rl.config(text=u, font=("Arial", int(size), "bold"))

def sync_p(event): #主視窗大小變化時
    w = root.winfo_width()
    h = root.winfo_height()
    rx = root.winfo_rootx()
    ry = root.winfo_rooty()
    b1.geometry(f"{int(h/2)}x{int(h/2)}+{rx+w}+{ry}")
    b2.geometry(f"{int(h/2)}x{int(h/2)}+{rx+w}+{int(ry+0.5*h)}")
    size = int(h/40)
    b1l.config(font=("Arial", size, "bold"))
    b2l.config(font=("Arial", size, "bold"))
    if x!='':
        c = len(x)
        size = w*h/c
        size = size ** 0.3
        word = int(w/(size*2.4))
        i=0
        u=""
        while i < c :
            u += x[i:i+word]
            u += "\n"
            i += word
        rl.config(text=u, font=("Arial", int(size), "bold"))


def r(event): #原文位置鎖定
    global is_d
    is_d *= -1
    if is_d==-1:
        #trans.withdraw()
        rx, ry, w, h= trans.winfo_rootx(),  trans.winfo_rooty(), trans.winfo_width(), trans.winfo_height()
        trans.overrideredirect(True)
        trans.geometry(f"{w}x{h}+{rx}+{ry}")
        trans.update_idletasks()
    else:
        #trans.deiconify()
        rx, ry, w, h = trans.winfo_rootx(),  trans.winfo_rooty(), trans.winfo_width(), trans.winfo_height()
        trans.overrideredirect(False)
        oy, ox =  trans.winfo_rooty()-trans.winfo_y(), trans.winfo_rootx()-trans.winfo_x()
        x, y = rx-ox, ry-oy
        trans.geometry(f"{w}x{h}+{x}+{y}")
        trans.update_idletasks()

    
def shot(event): #翻譯截圖
    if is_d==-1:
        x, y, w, h= trans.winfo_rootx(), trans.winfo_rooty(), trans.winfo_width(), trans.winfo_height()
        s = pyautogui.screenshot(region=(x, y, w, h))
        ima2string(s)
    else:
        size = 60
        rl.config(text="請先固定原文位置", font=("Arial", size, "bold"))

def ima2string(img): #圖片文字化
    t = pytesseract.image_to_string(img, lang='eng')
    if t!="":
        calltrans(t)
    else:
        size = 60
        rl.config(text="空", font=("Arial", size, "bold"))

def open(event): #打開主視窗
    global is_d
    b1.deiconify()
    b2.deiconify()
    if is_d==1:
        trans.deiconify()

def icon(event): #收起主視窗
    b1.withdraw()
    b2.withdraw()
    trans.withdraw()

root = tk.Tk()
root.geometry("400x200+500+500")
root.title("翻譯")
root.attributes("-topmost", 1)
rl = tk.Label(root, text="", anchor='w', justify='left')
rl.pack(anchor='w')#, padx=10, pady=10)
root.bind('<Configure>',sync_p)
root.bind("<Map>", open)
root.bind("<Unmap>", icon)

trans = tk.Toplevel()
trans.geometry("400x200+200+200")
trans.title("原文")
trans.attributes("-alpha", 0.5)
trans.attributes("-topmost", 2)

b1 = tk.Toplevel()
b1.config(bg="#086776")
b1.overrideredirect(True)
b1.attributes("-topmost", 1)
b1l = tk.Label(b1, text="固定/修改\n原文位置", font=(5), fg="white", bg="#086776")
b1l.pack(expand=True)
b1.bind('<Button-1>', r)

b2 = tk.Toplevel()
b2.config(bg="red")
b2l = tk.Label(b2, text="翻譯", font=(5), fg="white", bg="red")
b2l.pack(expand=True)
b2.overrideredirect(True)
b2.attributes("-topmost", 1)
b2.bind('<Button-1>', shot)

root.mainloop()
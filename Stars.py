def indexer(stroka):
    star = []
    HR, name, RAh, RAm, RAs, DEd, DEm, DEs, Vmag = stroka[0:4], stroka[4:14], \
                                                   stroka[75:77], stroka[77:79], stroka[79:83], \
                                                   stroka[83:86], stroka[86:88], stroka[88:90], \
                                                   stroka[102:107]
    try:
        star.append(int(HR))
        star.append(name)
        star.append((float(RAh) + float(RAm) / 60 + float(RAs) / 3600) / 24 * 360)
        star.append((float(DEd) + float(DEm) / 60 + float(DEs) / 3600))
        star.append(float(Vmag))
    except ValueError:
        star = None
    return star


all_stars = []
# 424 - Polar Star
with open("catalog", 'r', encoding='utf-8', errors='ignore') as fdata:
    for line in fdata:
        res = indexer(line)
        if res != None:
            all_stars.append(res)

import numpy as np


def RotX(a):
    return np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])


def RotY(a):
    return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])


def RotZ(a):
    return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])


g = np.radians(1)  #
p = np.radians(0)  # ориентация объектива
l = np.radians(0)  #
w = 7  # 15 град - угол поля зрения 2w
k = 1 / np.tan(np.radians(w / 2))
eps = 1e-6
minVmag = 6  # 5.9 # максимальная регистрируемая звездная величина
n = RotX(g) @ RotY(p) @ RotZ(l)
isTest = False
is_update = True

from pynput import keyboard
from tkinter import *

root = Tk()
canvas = Canvas(root, bg="black")
canvas.pack(side="bottom", fill="both", expand=True)

root2 = Tk()
canvas2 = Canvas(root2, bg="black")
canvas2.pack(side="bottom", fill="both", expand=True)

from PIL import ImageGrab


def save_canvas():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    xx = x + canvas.winfo_width()
    yy = y + canvas.winfo_height()

    name = "cam"
    if isTest:
        name = "dots"
    ImageGrab.grab(bbox=(x + 5, y + 5, xx - 5, yy - 5)).save(name + "_1.bmp", "BMP")

    x = root2.winfo_rootx() + canvas2.winfo_x()
    y = root2.winfo_rooty() + canvas2.winfo_y()
    xx = x + canvas2.winfo_width()
    yy = y + canvas2.winfo_height()
    ImageGrab.grab(bbox=(x + 5, y + 5, xx - 5, yy - 5)).save(name + "_2.bmp", "BMP")


def DrawStar(c, yz, zz, Vmag):
    ym = (c.winfo_width()) / 2
    zm = (c.winfo_height()) / 2

    kk = 0.736648
    ys = ym - kk * yz * zm
    zs = zm + kk * zz * zm

    if ys < ym * 2 and ys > 0 and zs < zm * 2 and zs > 0 and Vmag < minVmag:
##        c.create_oval(ys, zs, ys + (minVmag - Vmag) * 3, zs + (minVmag - Vmag) * 3, fill='white')
        c.create_oval(ys, zs, ys + 1, zs + 1, fill='white')

def Draw(c, n):
    global isMove
    if isTest:
        c.delete("all")
        k = 1 / np.tan(np.radians(w / 2))
        for i in range(-1, 2):
            for j in range(-1, 2):
                ##                          RA = np.radians(w/2*i)
                ##                          DE = np.radians(w/2*j)
                ##                          stCoords = (RotY(DE)@RotZ(RA)).T@np.array([1,0,0])
                ##                          yz = stCoords[1]*k/stCoords[0]
                ##                          zz = stCoords[2]*k/stCoords[0]
                ##                          print(yz, zz)
                yz = i * 2 / 3
                zz = j * 2 / 3
                DrawStar(c, yz, zz, minVmag - 2)
        return None

    c.delete("all")
    k = 1 / np.tan(np.radians(w / 2))
    for st in all_stars:
        RA = np.radians(st[2])
        DE = np.radians(st[3])
        stCoords = (RotY(DE) @ RotZ(RA)).T @ np.array([1, 0, 0])
        newCoords = n @ stCoords
        if newCoords[0] > eps:
            yz = newCoords[1] * k / newCoords[0]
            zz = newCoords[2] * k / newCoords[0]
            DrawStar(c, yz, zz, st[4])


noF = 0
isSave = False


def on_press(key):
    global x
    global y
    global n
    global w
    global isTest
    global noF
    global isSave
    global is_update
    is_update = True
    an = np.radians(1)
    if key == keyboard.Key.up:
        n = RotY(-an) @ n
    if key == keyboard.Key.down:
        n = RotY(an) @ n
    if key == keyboard.Key.right:
        n = RotZ(an) @ n
    if key == keyboard.Key.left:
        n = RotZ(-an) @ n
    if key == keyboard.Key.page_down:
        n = RotX(-an) @ n
    if key == keyboard.Key.end:
        n = RotX(an) @ n
    if key == keyboard.KeyCode.from_char('-'):
        w += 1
    if key == keyboard.KeyCode.from_char('+'):
        w -= 1
    if key == keyboard.Key.tab:
        isTest = not isTest
    if key == keyboard.Key.f2:
        noF += 1
        isSave = True


def on_release(key):
    ##    print('{0} released'.format(
    ##        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
##with keyboard.Listener(
##        on_press=on_press,
##        on_release=on_release) as listener:
##    listener.join()


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

# print(RotY(np.radians(90)) @ n)

while listener.running:
    Draw(canvas, RotY(np.radians(90)) @ n)
    Draw(canvas2, RotY(np.radians(-90)) @ n)
    root.update()
    root2.update()
    if isSave:
        root.after(1000, save_canvas)
        isSave = False
        print("ok")
root.destroy()
root2.destroy()

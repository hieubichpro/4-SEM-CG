from tkinter import *
from tkinter import ttk
from info import *
from math import fabs, floor, sin, cos, radians
from numpy import sign
import numpy as np
from matplotlib import colors
from tkinter import colorchooser
from colormap import rgb2hex
import tkinter.messagebox as box
from datetime import datetime
import matplotlib.pyplot as plt

img = 0
curColorLines = ((0, 0, 0), '#000000') 

curColorBackground = ((255, 255, 255), '#FFFFFF')
I = 255
intensities = []

def create_menu(window):
    menubar = Menu(window)
    
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label='Выход', command=window.destroy)
    menubar.add_cascade(label='Файл', menu=filemenu)
    
    infomenu = Menu(menubar, tearoff=0)
    infomenu.add_command(label='О авторе', command=about_author)
    infomenu.add_command(label = 'О программе', command=about_task)
    menubar.add_cascade(label='Информация', menu=infomenu)
    
    window.config(menu=menubar)

def make_label(window, text_label, pos_x, pos_y):
    my_label = Label(window, text = text_label)
    my_label.place(relx = pos_x, rely=pos_y)

def create_label(window):
    make_label(window, "Алгоритм построения", 0.02, 0.04)
    make_label(window, "Начальная точка", 0.02, 0.1) 
    make_label(window, "Конечная точка", 0.02, 0.16) 
    make_label(window, "X: ", 0.15, 0.1)
    make_label(window, "Y: ", 0.22, 0.1)
    make_label(window, "X: ", 0.15, 0.16)
    make_label(window, "Y: ", 0.22, 0.16)
    make_label(window, "Построение спектр отрезков", 0.02, 0.45)
    make_label(window, "Центр спектра", 0.01, 0.53)
    make_label(window, "X: ", 0.085, 0.53)
    make_label(window, "Y: ", 0.225, 0.53)
    make_label(window, "Угловой шаг: ", 0.02, 0.57)
    make_label(window, "Длина: ", 0.2, 0.57)
    

def create_button(window, main_canvas, line_canvas, bg_canvas, all_entry, list_box):
    chooselineColor = Button(window, text = "Цвет линии", command= lambda: chooseLineColor(line_canvas))
    chooselineColor.place(relx = 0.04, rely = 0.22)
    
    chooseFontColor = Button(window, text="Цвет фона", command=lambda: chooseBackgroundColor(main_canvas, bg_canvas))
    chooseFontColor.place(relx = 0.19, rely = 0.22)
    
    buildLine = Button(window, text = "Построить отрезок", command=lambda: process_and_build(all_entry[0], all_entry[1], list_box, main_canvas))
    buildLine.place(relx=0.1, rely = 0.29)
    
    buildSpekt= Button(window, text = "Построить спектр", command = lambda : bunchResearch(all_entry[2], all_entry[3], all_entry[4], list_box, main_canvas))
    buildSpekt.place(relx = 0.1, rely = 0.62)
    
    researchTime = Button(window, text = "Исследование временных характеристик алгоритмов", command=lambda: time_comparison(main_canvas))
    researchTime.place(relx = 0.02, rely = 0.7, relheight=0.07)
    
    researchStep = Button(window, text = "Исследование ступенчатости отрезков", command=step_comparison)
    researchStep.place(relx = 0.05, rely = 0.78, relheight=0.07)
    
    cleanBtn = Button(window, text = "Очистить экран", command=lambda: clear_canvas(main_canvas))
    cleanBtn.place(relx=0.1, rely=0.88, relheight=0.08)
    
def create_entry(window):
    xStart = Entry(window)
    xStart.place(relx = 0.17, rely=0.1, relwidth=0.03)
    xStart.insert(0, "100")
    yStart = Entry(window)
    yStart.place(relx = 0.24, rely=0.1, relwidth=0.03)
    yStart.insert(0, "100")
    xEnd = Entry(window)
    xEnd.place(relx = 0.17, rely=0.16, relwidth=0.03)
    xEnd.insert(0, "300")
    yEnd = Entry(window)
    yEnd.place(relx = 0.24, rely=0.16, relwidth=0.03)
    yEnd.insert(0, "105")
    centerX = Entry(window)
    centerX.place(relx=0.1, rely=0.53, relwidth=0.04)
    centerX.insert(0, "0")
    centerY = Entry(window)
    centerY.place(relx=0.24, rely=0.53, relwidth=0.04)
    centerY.insert(0, "0")
    angle = Entry(window)
    angle.place(relx=0.1, rely=0.57, relwidth=0.04)
    angle.insert(0, "5")
    length= Entry(window)
    length.place(relx=0.24, rely=0.57, relwidth=0.04)
    length.insert(0, "100")
    return [[xStart, yStart], [xEnd, yEnd], angle, length, [centerX, centerY]]

def create_canvas(window):
    canvas = Canvas(window, width=820, height=720, background='white')
    canvas.place(relx=0.35, rely=0)
    global img
    img = PhotoImage(width=820, height=720)
    canvas.create_image((410, 360), image=img, state='normal')
    draw_center(canvas)
    bg_canvas = Canvas(window, bg = curColorBackground[1], borderwidth = 5, relief = RIDGE, width = 40, height = 20)
    bg_canvas.place(relx=0.245, rely=0.215)
    line_canvas = Canvas(window, bg = curColorLines[1], borderwidth = 5, relief = RIDGE, width = 40, height = 20)
    line_canvas.place(relx=0.1, rely=0.215)
    return canvas, line_canvas, bg_canvas

def draw_center(canvas):
    w = canvas.winfo_reqwidth() - 4
    h = canvas.winfo_reqheight() - 4
    
    canvas.create_oval(w/2-1.5, h/2+1.5, 
                       w/2+1.5, h/2-1.5, fill='red')
    
    canvas.create_text(w/2, h/2 - 2 * 5, 
                       text = "%s(%d,%d)" %("O", 0,0),
                        font = ("Courier New", 8, "bold"), fill = "darkmagenta")

def create_listbox(window):
    listBox = ttk.Combobox(window, width = 40, textvariable = 0, state = 'readonly', values =
    ('1. Алгоритм ЦДА',
     '2. Алгоритм Брезенхема(float)',
     '3. Алгоритм Брезенхема(int)',
     '4. Алгоритм Брезенхема со сглаживанием',
     '5. Алгоритм Ву',
     '6. Алгоритм Tkinter canvas.create_line'))
    listBox.place(relx=0.14, rely=0.04)
    listBox.current(0)
    return listBox

def to_screen_coord(my_canvas, x, y):
    width = my_canvas.winfo_reqwidth() - 4
    height = my_canvas.winfo_reqheight() - 4
    return int(x + width / 2), int(-y + height / 2)

def my_round(number):
    ret = int(number)
    if number < 0:
        if fabs(number) - abs(ret) >= 0.5:
            return ret - 1
        else:
            return ret
    else:
        if number - ret >= 0.5:
            return ret + 1
        else:
            return ret


def DDA(xStart, yStart, xEnd, yEnd, draw = True, count_step = False):
    if xStart == xEnd and yStart == yEnd:
        img.put(curColorLines, (xStart, yStart))
        return
    deltaX = xEnd - xStart
    deltaY = yEnd - yStart

    L = fabs(deltaX) if fabs(deltaX) >= fabs(deltaY) else fabs(deltaY)

    dx = deltaX / L
    dy = deltaY / L
    
    curX = xStart
    curY = yStart
    
    x_buff, y_buff = curX, curY
    step = 0
    
    for _ in range(int(L)):
        x_draw, y_draw = my_round(curX), my_round(curY)
        if draw: 
            img.put(curColorLines[1], (x_draw, y_draw))
            
        curX += dx
        curY += dy
        
        if count_step:
            if my_round(x_buff) != my_round(curX) and my_round(y_buff) != my_round(curY):
                step += 1
            x_buff, y_buff = curX, curY
            
    return step if count_step else None

def realBresenham(xStart, yStart,xEnd, yEnd, draw = True, step_count = False):
    if xStart == xEnd and yStart == yEnd:
        img.put(curColorLines[1], (xStart, yStart))
        return

    deltaX = xEnd - xStart
    deltaY = yEnd - yStart

    stepX = int(sign(deltaX))
    stepY = int(sign(deltaY))

    deltaX = abs(deltaX)
    deltaY = abs(deltaY)

    if deltaX < deltaY:
        deltaX, deltaY = deltaY, deltaX
        flag = True
    else:
        flag = False

    m = deltaY / deltaX

    c = m - 0.5
    curX = xStart
    curY = yStart
    
    x_buff, y_buff = curX, curY
    step = 0

    for _ in range(deltaX):
        if draw: img.put(curColorLines[1], (curX, curY))     
        
        if flag:
            if c >= 0:
                curX += stepX
                c -= 1
            curY += stepY
            c += m
        else:
            if c >= 0:
                curY += stepY
                c -= 1
            curX += stepX
            c += m
            
        if step_count:
            if curX != x_buff and curY != y_buff:
                step += 1
            x_buff, y_buff = curX, curY
            
    return step if step_count else None

def intBresenham(xStart, yStart, xEnd, yEnd, draw = True, step_count = False):
    if xStart == xEnd and yStart == yEnd:
        img.put(curColorLines[1], (xStart, yStart))
        return

    deltaX = xEnd - xStart
    deltaY = yEnd - yStart

    stepX = int(sign(deltaX))
    stepY = int(sign(deltaY))

    deltaX = abs(deltaX)
    deltaY = abs(deltaY)

    if deltaX < deltaY:
        deltaX, deltaY = deltaY, deltaX
        flag = True
    else:
        flag = False

    acc = deltaY + deltaY - deltaX
    curX = xStart
    curY = yStart
    
    x_buff, y_buff = curX, curY
    step = 0

    for i in range(deltaX):
        if draw:
            img.put(curColorLines[1], (curX, curY))

        if flag:
            if acc >= 0:
                curX += stepX
                acc -= deltaX + deltaX
            curY += stepY
            acc += deltaY + deltaY
        else:
            if acc >= 0:
                curY += stepY
                acc -= deltaX + deltaX
            curX += stepX
            acc += deltaY + deltaY
            
        if step_count:
            if curX != x_buff and curY != y_buff:
                step += 1
            x_buff, y_buff = curX, curY
            
    return step if step_count else None

def stepRemovalBresenham(xStart, yStart, xEnd, yEnd, draw = True, step_count = False):
    dx = xEnd - xStart
    dy = yEnd - yStart

    if dx == 0 and dy == 0:
        img.put(curColorLines[1], (xStart, yStart))

    x_sign = int(sign(dx))
    y_sign = int(sign(dy))

    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        flag = 1
    else:
        flag = 0

    m = dy / dx * I
    w = I - m    
    e = I / 2
    
    curX = xStart
    curY = yStart

    x_buff, y_buff = curX, curY
    step = 0

    for _ in range(dx):
        color = intensities[I - my_round(e) - 1]
        if draw: img.put(color, (curX, curY))

        if e < w:    #Если ордината соседнего пиксела не увеличивается
            if flag:
                curY += y_sign
            else:
                curX += x_sign
    
            e += m

        else:       # ордината соседнего пиксела увеличивается на единицу
            curX += x_sign
            curY += y_sign
            e -= w  # необходимо вычесть величину площади пиксела, то есть единицу: e=e+m-1
            
        if step_count:
            if curX != x_buff and curY != y_buff:
                step += 1
            x_buff, y_buff = curX, curY
            
    return step if step_count else None
            
def WuAlg(xStart, yStart, xEnd, yEnd, draw = True):

    if xStart == xEnd and yStart == yEnd:
        img.put(curColorLines[1], (xStart, yStart))
    
    flag = abs(yEnd - yStart) > abs(xEnd - xStart)

    if flag:
        xStart, yStart = yStart, xStart
        xEnd, yEnd = yEnd, xEnd
    if xStart > xEnd:
        xStart, xEnd = xEnd, xStart
        yStart, yEnd = yEnd, yStart

    dx = xEnd - xStart
    dy = yEnd - yStart

    if dx == 0:
        tg = 1
    else:
        tg = dy / dx

    xStart = int(xStart)
    xEnd = int(xEnd + 0.5)
    
    y = yStart + tg

    if flag:
        for x in range(xStart, xEnd):
            color1 = intensities[int(254 * (abs(1 - fabs(y - int(y)))))]
            color2 = intensities[int(254 * (abs(y - int(y))))]
            if draw:
                img.put(color1, (int(y) + 1, x))
                img.put(color2, (int(y), x))
            y += tg
    else:
        for x in range(xStart, xEnd):
            color1 = intensities[int(254 * (abs(1 - y + floor(y))))]
            color2 = intensities[int(254 * (abs(y - floor(y))))]
            if draw:
                img.put(color1, (x, int(y) + 1))
                img.put(color2, (x, int(y)))
            y += tg
        
def count_step_wu(one_point, two_point):
    x1 = one_point[0]
    y1 = one_point[1]
    x2 = two_point[0]
    y2 = two_point[1]

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return 0

    m = 1
    step = 1
    steps = 0

    if (abs(dy) >= abs(dx)):
        if (dy != 0):
            m = dx / dy
            
        m1 = m

        if (y1 > y2):
            m1 *= -1
            step *= -1

        bord = round(y2) - 1 if dy < dx else round(y2) + 1

        for y in range(round(y1), bord, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1

            if y < round(y2) and int(x1) != int(x1 + m):
                steps += 1

            x1 += m1
    else:
        if (dx != 0):
            m = dy / dx

        m1 = m

        if (x1 > x2):
            step *= -1
            m1 *= -1

        bord = round(x2) - 1 if dy > dx else round(x2) + 1

        for x in range(round(x1), bord, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1

            if x < round(x2) and int(y1) != int(y1 + m):
                steps += 1

            y1 += m1

    return steps

def libAlgo(canvas, xStart, yStart, xEnd, yEnd, draw = True):
    if draw:
        canvas.create_line(xStart, yStart, xEnd, yEnd, width = 1, fill = curColorLines[1])
            
def chooseLineColor(canvas_color_line):
    global curColorLines
    curColorLines = colorchooser.askcolor()
    canvas_color_line.config(bg = curColorLines[1])

def chooseBackgroundColor(my_canvas, canvas_color_bg):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()
    canvas_color_bg.config(bg = curColorBackground[1])
    my_canvas.config(bg = curColorBackground[1])

# Массив цветов одного оттенка разной интенсивности
def get_rgb_intensity(color, bg_color):
    grad = []
    r_ratio = float(bg_color[0] - color[0]) / I # получение шага интенсивности
    g_ratio = float(bg_color[1] - color[1]) / I
    b_ratio = float(bg_color[2] - color[2]) / I
    for i in range(I):
        nr = int(color[0] + (r_ratio * i)) # заполнение массива разными оттенками
        ng = int(color[1] + (g_ratio * i))
        nb = int(color[2] + (b_ratio * i))
        grad.append("#%2.2x%2.2x%2.2x" % (nr, ng, nb))
    # grad.reverse()
    return grad

def build_line(xStart,yStart, xEnd, yEnd, combo, main_canvas):
    xStart, yStart = to_screen_coord(main_canvas, xStart, yStart)
    xEnd, yEnd = to_screen_coord(main_canvas, xEnd, yEnd)
    algo = combo.get()
    
    if algo[0] == "1":
        DDA(xStart, yStart, xEnd, yEnd)
    elif algo[0] == "2":
        realBresenham(xStart, yStart, xEnd, yEnd)
    elif algo[0] == "3":
        intBresenham(xStart, yStart,xEnd, yEnd)
    elif algo[0] == "6":
        libAlgo(main_canvas, xStart, yStart, xEnd, yEnd)
    else:
        global intensities
        intensities = get_rgb_intensity(curColorLines[0], curColorBackground[0])
        if algo[0] == "4":
            stepRemovalBresenham(xStart, yStart,xEnd, yEnd)
        else:
            WuAlg(xStart ,yStart, xEnd, yEnd)
        

def process_and_build(start_entry, end_entry, list_box, main_canvas):
    try:
        xStart = int(start_entry[0].get())
        yStart = int(start_entry[1].get())
        xEnd = int(end_entry[0].get())
        yEnd = int(end_entry[1].get())
    except:
        if (not start_entry[0].get()) or (not start_entry[1].get()) or (not end_entry[0].get()) or (not end_entry[1].get()):
            box.showerror("Ошибка", "Пустой ввод")
        else:
            box.showerror("Ошибка", "Координаты должны быть целыми")
        return
    build_line(xStart, yStart, xEnd, yEnd, list_box, main_canvas)


def bunchResearch(degree, length, center, combo, canvasWindow):
    try:
        degreesStep = float(degree.get())
    except:
        box.showerror("Ошибка", "Угловой шаг должен быть целым")
        return

    try:
        length = int(length.get())
        if length <= 0:
            box.showerror("Ошибка", "Длина должна быть положительным")
            return
    except:
        box.showerror("Ошибка", "Длина должна быть действительным")
        return

    try:
        centerX = int(center[0].get())
        centerY = int(center[1].get())
    except:
        box.showerror("Ошибка", "Координаты центра должны быть целыми числами")
        return
    degrees = 0
    xEnd = centerX + length
    yEnd = centerY
    while abs(degrees) < 360:
        build_line(centerX, centerY, xEnd, yEnd, combo, canvasWindow)
        degrees += degreesStep
        xEnd = my_round(length * cos(radians(degrees))) + centerX
        yEnd = my_round(length * sin(radians(degrees))) + centerY

def time_comparison(canvasWindow):
    masTime = []
    curTime = 0

    global intensities
    intensities = get_rgb_intensity(curColorLines[0], curColorBackground[0])    

    for i in range(1000):
        degrees = 0
        curX = 510
        curY = 360
        while abs(degrees) <= 360:
            
            start = datetime.now()
            DDA(410, 360, curX, curY, False)
            end = datetime.now()
            
            curTime = curTime + (end.timestamp() - start.timestamp())
            
            degrees += 20
            curX = my_round(100 * cos(radians(degrees)) + 410)
            curY = my_round(100 * sin(radians(degrees)) + 360)
    curTime /= 1500
    masTime.append(curTime)
    curTime = 0

    for i in range(1000):
        curX = 510
        curY = 360
        degrees = 0
        while abs(degrees) <= 360:
            
            start = datetime.now()
            realBresenham(410, 360, curX, curY, False)
            end = datetime.now()
            
            curTime = curTime + (end.timestamp() - start.timestamp())
            
            degrees += 20
            curX = my_round(100 * cos(radians(degrees))+ 410)
            curY = my_round(100 * sin(radians(degrees)) + 360)
    curTime /= 900
    masTime.append(curTime)
    curTime = 0

    for i in range(1000):
        curX = 510
        curY = 360
        degrees = 0
        while abs(degrees) <= 360:
            
            start = datetime.now()
            intBresenham(410, 360, curX, curY, False)
            end = datetime.now()
            
            curTime = curTime + (end.timestamp() - start.timestamp())
            
            degrees += 20
            curX = my_round(100 * cos(radians(degrees)) + 410)
            curY = my_round(100 * sin(radians(degrees)) + 360)
    curTime /= 1200
    masTime.append(curTime)
    curTime = 0

    for i in range(1000):
        degrees = 0
        curX = 510
        curY = 360
        while abs(degrees) <= 360:
            
            start = datetime.now()
            stepRemovalBresenham(410, 360, curX, curY, False)
            end = datetime.now()
            
            curTime = curTime + (end.timestamp() - start.timestamp())
            
            degrees += 20
            curX = my_round(100 * cos(radians(degrees)) + 410)
            curY = my_round(100 * sin(radians(degrees)) + 360)
    curTime /= 600
    masTime.append(curTime)
    curTime = 0

    for i in range(1000):
        degrees = 0
        curX = 510
        curY = 360
        while abs(degrees) <= 360:
            
            start = datetime.now()
            WuAlg(410, 360, curX, curY, False)
            end = datetime.now()
            
            curTime = curTime + (end.timestamp() - start.timestamp())
            
            degrees += 20
            curX = my_round(100 * cos(radians(degrees)) + 410)
            curY = my_round(100 * sin(radians(degrees)) + 360)
    curTime /= 600
    masTime.append(curTime)
    curTime = 0

    for i in range(1000):
        degrees = 0
        curX = 510
        curY = 360
        while abs(degrees) <= 360:
            
            start = datetime.now()
            libAlgo(canvasWindow, 410, 360, curX, curY, True)
            degrees += 20
            curX = my_round(100 * cos(radians(degrees)) + 410)
            curY = my_round(100 * sin(radians(degrees)) + 360)
            end = datetime.now()
            
            curTime = curTime + (end.timestamp() - start.timestamp())
            
    curTime /= 1000
    masTime.append(curTime)
    plt.figure(figsize = (18, 10))
    masNames = ["ЦДА", "Брезенхем \n(float)",
                "Брезенхем \n(int)", "Брезенхем \n(со сглаживанием)",
                "Ву", "Библиотечная\nфункция"]

    plt.bar(masNames, masTime, align = "center")
    plt.title("Временные характеристики алгоритмов")
    plt.ylabel("Затраченное время")
    plt.xlabel("Алгоритм")
    plt.show()
    clear_canvas(canvasWindow)
    
def step_comparison():
    
    global intensities
    intensities = get_rgb_intensity(curColorLines[0], curColorBackground[0])
    
    dda_list = []
    bres_float_list = []
    bres_int_list = []
    bres_antial_list = []
    wu_list = []

    angle = 0
    angle_step = 2
    curX = 510
    curY = 360
    while angle <= 90:
        dda_list.append(DDA(410, 360, curX, curY, False, True))
        bres_float_list.append(realBresenham(410, 360, curX, curY, False, True))
        bres_int_list.append(intBresenham(410, 360, curX, curY, False, True))
        bres_antial_list.append(stepRemovalBresenham(410, 360, curX, curY, False, True))
        wu_list.append(count_step_wu([410, 360], [curX, curY]))

        angle += angle_step
        curX = my_round(410 + 100*cos(radians(angle)))
        curY = my_round(360 - 100*sin(radians(angle)))
    
    angle_list = [i for i in range(0, 91, 2)]
    for i in range (23):
        wu_list[45 - i] = wu_list[i]
    plt.figure(figsize = (10, 6))
    plt.rcParams['font.size'] = '14'

    plt.plot(angle_list, dda_list, label = 'ЦДА')
    plt.plot(angle_list, bres_float_list, linestyle = '--', label = 'Брезенхем\n(float)')
    plt.plot(angle_list, bres_float_list, linestyle = 'dotted', label = 'Брезенхем\n(int)')
    plt.plot(angle_list, bres_antial_list, label = 'Брезенхем\n(с устранением\nступенчатости)',
        linestyle = '-.')
    plt.plot(angle_list, wu_list, label = 'Ву', linestyle = ':')

    plt.title("Исследование ступенчатости.\n{0} - длина отрезка".format(100))
    plt.legend()
    plt.xticks(np.arange(91, step = 5))
    plt.ylabel("Колличество ступенек")
    plt.xlabel("Угол в градусах")
    plt.show()
    
def clear_canvas(canvas):
    canvas.delete("all")
    global img
    img = PhotoImage(width=820, height=720)
    canvas.create_image((410, 360), image=img, state='normal')
    draw_center(canvas)
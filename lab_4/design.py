from tkinter import *
from tkinter import ttk
from info import *
from math import fabs, floor, sin, cos, radians
import numpy as np
from matplotlib import colors
from tkinter import colorchooser
from colormap import rgb2hex
import tkinter.messagebox as box
from datetime import datetime
import matplotlib.pyplot as plt
from my_functions import *
from circle_algo import canonicalCircleAlg, parameterCircleAlg, bresenhamCircleAlg, middlePointCircleAlg
from ellipse_algo import canonicalEllipseAlg, parameterEllipseAlg, bresenhamEllipseAlg, middlePointEllipseAlg

canvas = 0
img = 0
curColorLines = '#000000'
curColorBackground = '#FFFFFF'

def chooseLineColor(canvas_color_line):
    global curColorLines
    curColorLines = colorchooser.askcolor()[1]
    canvas_color_line.config(bg = curColorLines)

def chooseBackgroundColor(my_canvas, canvas_color_bg):
    global curColorBackground
    curColorBackground = colorchooser.askcolor()[1]
    canvas_color_bg.config(bg = curColorBackground)
    my_canvas.config(bg = curColorBackground)

def clear_canvas(canvas):
    canvas.delete("all")
    global img
    img = PhotoImage(width=820, height=720)
    canvas.create_image((410, 360), image=img, state='normal')
    draw_center(canvas)

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

def create_label(window):
    make_label(window, "Алгоритм построения", 0.02, 0.01)
    make_label(window, "Тип кривой", 0.05, 0.05) 
    make_label(window, "ПАРАМЕТРЫ ФИГУРЫ", 0.02, 0.17)
    make_label(window, "Центр по X: ", 0.02, 0.22)
    make_label(window, "Центр по Y: ", 0.19, 0.22)

    R_label = Label(window, text = "R: ")
    R_a_label = Label(window, text = "R_a: ")
    R_b_label = Label(window, text = "R_b: ")
    
    make_label(window, "ПАРАМЕТРА СПЕКТРА", 0.02, 0.45)
    make_label(window, "Центр по X: ", 0.05, 0.5)
    make_label(window, "Центр по Y: ", 0.19, 0.5)
    
    step_circle = Label(window, text = "Шаг: ")
    quantity_circle = Label(window, text = "N: ")
    r_start = Label(window, text = "R_нач: ")
    r_end = Label(window, text = "R_кон")
    hidden_label = Label(window, text = "Скрыть: ")
    
    r_a = Label(window, text = "R_a: ")
    r_b = Label(window, text = "R_b: ")
    step_a = Label(window, text = "Шаг_a: ")
    step_b = Label(window, text = "Шаг_b")
    quantity_ellipse = Label(window, text = "Количество")
    R_label.place(relx = 0.12, rely = 0.27)
    r_start.place(relx = 0.02, rely = 0.55)
    r_end.place(relx = 0.10, rely = 0.55)
    step_circle.place(relx = 0.18, rely = 0.55)
    quantity_circle.place(relx = 0.26, rely = 0.55)
    hidden_label.place(relx = 0.03, rely = 0.60)  
    
    return [[R_label, R_a_label, R_b_label], [r_start, r_end, step_circle, quantity_circle, hidden_label], [r_a, r_b, step_a, step_b, quantity_ellipse]]
        
    
def create_radioButton(label, entry):
    option_hidden = IntVar()
    option_hidden.set(2)
    
    r_start = Radiobutton(text = "R_нач", variable = option_hidden, value = 1, command = lambda: change_option(option_hidden, entry))
    r_start.place(relx = 0.03, rely =0.63)
    
    r_end = Radiobutton(text = "R_кон", variable = option_hidden, value = 2, command = lambda: change_option(option_hidden, entry))
    r_end.place(relx = 0.1, rely =0.63)
    
    quantity = Radiobutton(text = "N", variable = option_hidden, value = 3, command = lambda: change_option(option_hidden, entry))
    quantity.place(relx = 0.17, rely =0.63)

    step = Radiobutton(text = "Шаг", variable = option_hidden, value = 4, command = lambda: change_option(option_hidden, entry))
    step.place(relx = 0.24, rely =0.63)
    

    option_figure = IntVar()
    option_figure.set(1)
    
    figure_circle = Radiobutton(text = "Окружность", variable = option_figure, value = 1, command = lambda: change_figure(option_figure, label, entry, [r_start, r_end, quantity, step]))
    figure_circle.place(relx = 0.14, rely =0.05)

    figure_ellips = Radiobutton(text = "Эллипс", variable = option_figure, value = 2, command = lambda: change_figure(option_figure, label, entry, [r_start, r_end, quantity, step]))
    figure_ellips.place(relx = 0.24, rely =0.05)
    
    return option_figure, option_hidden
    
def create_button(window, main_canvas, line_canvas, bg_canvas, all_entry, comboAlgo, option, option_spekt_circle):
    xCenterEntry, yCenterEntry = all_entry[0]
    radiusCircleEntry, radiusA, radiusB = all_entry[1]
    xCenterSpekt, yCenterSpekt = all_entry[2]
    
    chooselineColor = Button(window, text = "Цвет линии", command= lambda: chooseLineColor(line_canvas))
    chooselineColor.place(relx = 0.04, rely = 0.115)
    
    chooseFontColor = Button(window, text="Цвет фона", command=lambda: chooseBackgroundColor(main_canvas, bg_canvas))
    chooseFontColor.place(relx = 0.19, rely = 0.115)
    
    buildFigura = Button(window, text = "Построить фигуру", command=lambda: drawCurve(option, comboAlgo, xCenterEntry, yCenterEntry, radiusCircleEntry, radiusA, radiusB, main_canvas))
    buildFigura.place(relx=0.11, rely = 0.31, relheight=0.07)
    
    buildSpekt= Button(window, text = "Построить спектр", command = lambda : spectralAnal(option, option_spekt_circle, comboAlgo, xCenterSpekt, yCenterSpekt, all_entry[3], all_entry[4], main_canvas))
    buildSpekt.place(relx = 0.115, rely = 0.69, relheight = 0.07)
    
    researchTime = Button(window, text = "Исследование временных характеристик алгоритмов", command=lambda: timeResearch(main_canvas, option))
    researchTime.place(relx = 0.04, rely = 0.78, relheight=0.07)
    
    cleanBtn = Button(window, text = "Очистить экран", command=lambda: clear_canvas(main_canvas))
    cleanBtn.place(relx=0.12, rely=0.88, relheight=0.08)
    
def create_entry(window):
    x_center = Entry(window)
    y_center = Entry(window)
    
    R_circle = Entry(window)
    R_a_ellipse = Entry(window)
    R_b_ellipse = Entry(window)
    
    #spekt
    x_center_spekt = Entry(window)
    y_center_spekt = Entry(window)
    
    step_r = Entry(window)
    N_circle = Entry(window)
    R_beg = Entry(window)
    R_end = Entry(window)
    
    step_a = Entry(window)
    step_b = Entry(window)
    R_a = Entry(window)
    R_b = Entry(window)
    N_ellipse = Entry(window)
    
    x_center.place(relx = 0.08, rely = 0.22, relwidth=0.04)
    y_center.place(relx = 0.25, rely = 0.22, relwidth=0.04)
    
    R_circle.place(relx = 0.14, rely = 0.27, relwidth=0.04)
    
    x_center_spekt.place(relx = 0.11, rely = 0.5, relwidth=0.04)
    y_center_spekt.place(relx = 0.25, rely = 0.5, relwidth=0.04)
    R_beg.place(relx = 0.05, rely = 0.55, relwidth=0.04)
    R_end.place(relx = 0.13, rely = 0.55, relwidth=0.04)
    R_end.configure(state = DISABLED)
    step_r.place(relx = 0.21, rely = 0.55, relwidth=0.04)
    N_circle.place(relx = 0.28, rely = 0.55, relwidth=0.04)
    
    x_center.insert(0, "0")
    y_center.insert(0, "0")
    R_circle.insert(0, "100")
    
    R_a_ellipse.insert(0, "120")
    R_b_ellipse.insert(0, "90")
    
    x_center_spekt.insert(0, "0")
    y_center_spekt.insert(0, "0")
    R_beg.insert(0, "50")
    step_r.insert(0, "10")
    N_circle.insert(0, "5")
    
    R_a.insert(0, "40")
    R_b.insert(0, "30")
    step_a.insert(0, "10")
    step_b.insert(0, "10")
    N_ellipse.insert(0, "10")
    
    return [[x_center, y_center], [R_circle, R_a_ellipse, R_b_ellipse], [x_center_spekt, y_center_spekt], [step_r, N_circle, R_beg, R_end], [step_a, step_b, R_a, R_b, N_ellipse]]

def create_canvas(window):
    global canvas
    canvas = Canvas(window, width=820, height=720, background='white')
    canvas.place(relx=0.35, rely=0)
    global img
    img = PhotoImage(width=820, height=720)
    canvas.create_image((410, 360), image=img, state='normal')
    draw_center(canvas)
    bg_canvas = Canvas(window, bg = curColorBackground, borderwidth = 5, relief = RIDGE, width = 40, height = 20)
    bg_canvas.place(relx=0.245, rely=0.11)
    line_canvas = Canvas(window, bg = curColorLines, borderwidth = 5, relief = RIDGE, width = 40, height = 20)
    line_canvas.place(relx=0.1, rely=0.11)
    return canvas, line_canvas, bg_canvas

def create_listbox(window):
    algoListBox = ttk.Combobox(window, width = 40, textvariable = 0, state = 'readonly', values =
    ('1. Каноническое уравнение',
     '2. Параметрическое уравнение',
     '3. Алгоритм Брезенхема',
     '4. Алгоритм средней точки',
     '5. Алгоритм Tkinter canvas.create_oval'))
    algoListBox.place(relx=0.14, rely=0.01)
    algoListBox.current(0)
    
    return algoListBox


def drawArr(image, pointsArray):
    for j in pointsArray:
        j[0], j[1] = to_screen_coord(canvas, j[0], j[1])
    
    for i in pointsArray:
        image.put(i[2], (i[0], i[1]))


def drawMiddlePointCircle(xCenter, yCenter, radius):
    drawArray = middlePointCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawBresenhamCircle(xCenter, yCenter, radius):
    drawArray = bresenhamCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawParameterCircle(xCenter, yCenter, radius):
    drawArray = parameterCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawCanonicalCircle(xCenter, yCenter, radius):
    drawArray = canonicalCircleAlg(xCenter, yCenter, radius, curColorLines)
    drawArr(img, drawArray)


def drawTkinterCircle(canvasWindow, xCenter, yCenter, radius):
    xCenter, yCenter = to_screen_coord(canvasWindow, xCenter, yCenter)
    canvasWindow.create_oval(xCenter - radius,
                             yCenter - radius, xCenter + radius,
                             yCenter + radius, outline = curColorLines)


def drawMiddlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY):
    drawArray = middlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY)
    drawArr(img, drawArray)


def drawBresenhamEllipse(xCenter, yCenter, radiusX, radiusY):
    drawArray = bresenhamEllipseAlg(xCenter, yCenter, radiusX, radiusY, curColorLines)
    drawArr(img, drawArray)


def drawParameterEllipse(xCenter, yCenter, radiusX, radiusY):
    drawArray = parameterEllipseAlg(xCenter, yCenter, radiusX, radiusY, curColorLines)
    drawArr(img, drawArray)


def drawCanonicalEllipse(xCenter, yCenter, radiusX, radiusY):
    drawArray = canonicalEllipseAlg(xCenter, yCenter, radiusX, radiusY, curColorLines)
    drawArr(img, drawArray)


def drawTkinterEllipse(xCenter, yCenter, radiusX, radiusY, canvasWindow):
    xCenter, yCenter = to_screen_coord(canvasWindow, xCenter, yCenter)
    canvasWindow.create_oval(xCenter - radiusX, yCenter - radiusY,
                             xCenter + radiusX, yCenter + radiusY,
                             outline = curColorLines)

def drawCircle(comboAlg, xCenterEnt, yCenterEnt, radiusEnt, canvasWindow):
    got = comboAlg.get()
    try:
        xCenter = int(xCenterEnt.get())
        yCenter = int(yCenterEnt.get())
        radius = int(radiusEnt.get())
    except:
        box.showerror("Ошибка", "Входные должны быть целыми")
        return

    if radius > 350:
        box.showerror("Ошибка", "Превышалось максимальное значение(350)")
        return

    alg = got[0]
    if alg == "1":
        drawCanonicalCircle(xCenter, yCenter, radius)
    elif alg == "2":
        drawParameterCircle(xCenter, yCenter, radius)
    elif alg == "3":
        drawBresenhamCircle(xCenter, yCenter, radius)
    elif alg == "4":
        drawMiddlePointCircle(xCenter, yCenter, radius)
    else:
        drawTkinterCircle(canvasWindow, xCenter, yCenter, radius)    
    
def drawEllipse(comboAlg, xCenterEnt, yCenterEnt, radiusXEnt, radiusYEnt, canvasWindow):
    got = comboAlg.get()
    try:
        xCenter = int(xCenterEnt.get())
        yCenter = int(yCenterEnt.get())
        radiusX = int(radiusXEnt.get())
        radiusY = int(radiusYEnt.get())
    except:
        box.showerror("Ошибка", "Входные должны быть целыми")
        return
    if radiusX > 400 or radiusY > 350:
        box.showerror("Ошибка", "Превышалось максимальное значение(400, 350)")
        return
    alg = got[0]
    
    if alg == "1":
        drawCanonicalEllipse(xCenter, yCenter, radiusX, radiusY)
    elif alg == "2":
        drawParameterEllipse(xCenter, yCenter, radiusX, radiusY)
    elif alg == "3":
        drawBresenhamEllipse(xCenter, yCenter, radiusX, radiusY)
    elif alg == "4":
        drawMiddlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY)
    else:
        drawTkinterEllipse(xCenter, yCenter, radiusX, radiusY, canvasWindow)

def drawCurve(option, comboAlg, xCenterEntry, yCenterEntry, radiusCir, radiusA, radiusB, canvasWindow):
    my_option = option.get()
    if my_option == 1:
        drawCircle(comboAlg, xCenterEntry, yCenterEntry, radiusCir, canvasWindow)
    else:
        drawEllipse(comboAlg, xCenterEntry, yCenterEntry, radiusA, radiusB, canvasWindow)     

def spectralAnal(option, option_spekt_circle, comboAlg, xCenter, yCenter, entryCircleSpekt, entryEllipseSpekt, canvasWindow):
    my_option = option.get()
    if my_option == 1:
        spectralCircles(comboAlg, option_spekt_circle, xCenter, yCenter, entryCircleSpekt, canvasWindow)
    else:
        spectralEllipse(comboAlg, xCenter, yCenter,entryEllipseSpekt, canvasWindow)

def spectralCircles(comboAlg, option_spekt_circle, xCenterEntry, yCenterEntry, entryCircleSpekt, canvasWindow):
    alg = comboAlg.get()[0]
    
    stepEntry, amountEntry, rBegEntry, rEndEntry = entryCircleSpekt
    try:
        xCenter = int(xCenterEntry.get())
        yCenter = int(yCenterEntry.get())
    except:
        box.showerror("Ошибка", "Входные данные должны быть целыми")
        return

    hidden_button = option_spekt_circle.get()

    if hidden_button == 1:
        try:
            rend = int(rEndEntry.get())
            step = int(stepEntry.get())
            amount = int(amountEntry.get())
        except:
            box.showerror("Ошибка", "Входные данные должны быть целыми")
            return
        if step <= 0 or amount <= 0 or rend <= 0:
            box.showerror("Ошибка", "Неверные данные")
            return
        rbeg = rend - (amount - 1) * step
        
    elif hidden_button == 2:
        try:
            rbeg = int(rBegEntry.get())
            step = int(stepEntry.get())
            amount = int(amountEntry.get())
        except:
            box.showerror("Ошибка", "Входные данные должны быть целыми")
            return
        if step <= 0 or rbeg <= 0 or amount <= 0:
            box.showerror("Ошибка", "Неверные данные")
            return
        rend = int(rbeg + (amount - 1) * step)
        
    elif hidden_button == 3:
        try:
            rbeg = int(rBegEntry.get())
            rend = int(rEndEntry.get())
            step = int(stepEntry.get())
        except:
            box.showerror("Ошибка", "Входные данные должны быть целыми")
            return
        if step <= 0 or rbeg <= 0 or rend <= 0:
            box.showerror("Ошибка", "Неверные данные")
            return
        amount = int((rend - rbeg) / step)
        rend = rbeg + step * amount
        
    elif hidden_button == 4:
        try:
            rbeg = int(rBegEntry.get())
            rend = int(rEndEntry.get())
            amount = int(amountEntry.get())
        except:
            box.showerror("Ошибка", "Входные данные должны быть целыми")
            return
        if amount <= 1 or rbeg <= 0 or rend <= 0:
            box.showerror("Ошибка", "Неверные данные")
            return
        step = (rend - rbeg) / (amount - 1)
        
    if rend > 350:
        box.showerror("Ошибка", "Превышалось максимальное значение(350)")
        return
    
    if alg == "1":
        spectralCanonicalCircle(xCenter, yCenter, rbeg, step, rend)
    if alg == "2":
        spectralParameterCircle(xCenter, yCenter, rbeg, step, rend)
    if alg == "3":
        spectralBresenhamCircle(xCenter, yCenter, rbeg, step, rend)
    if alg == "4":
        spectralMiddlePointCircle(xCenter, yCenter, rbeg, step, rend)
    if alg == "5":
        spectralTkinterCircle(xCenter, yCenter, rbeg, step, rend, canvasWindow)
        
def spectralEllipse(comboAlg, xCenter, yCenter,entryEllipseSpekt, canvasWindow):
    got = comboAlg.get()
    alg = got[0]

    stepXEntry, stepYEntry, xRadiusEntry, yRadiusEntry, NEntry = entryEllipseSpekt
    try:
        xCenter = int(xCenter.get())
        yCenter = int(yCenter.get())
        xRadius = int(xRadiusEntry.get())
        yRadius = int(yRadiusEntry.get())
        stepX = int(stepXEntry.get())
        stepY = int(stepYEntry.get())
        stop = int(NEntry.get())
    except:
        box.showerror("Ошибка", "Входные данные должны быть целыми")
    if xRadius + (stop - 1) * stepX > 400 or yRadius + (stop - 1) * stepY > 350:
        box.showerror("Ошибка", "Превышалось максимальное значение(400, 350)")
        return
    if alg == "1":
        spectralCanonicalEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "2":
        spectralParameterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "3":
        spectralBresenhamEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "4":
        spectralMiddlePointEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop)
    if alg == "5":
        spectralTkinterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop, canvasWindow)
    
def spectralTkinterCircle(xCenter, yCenter, radius, step, end, canvasWindow):
    for i in range(radius, end + step, step):
        drawTkinterCircle(canvasWindow, xCenter, yCenter, i)


def spectralMiddlePointCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawMiddlePointCircle(xCenter, yCenter, i)


def spectralBresenhamCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawBresenhamCircle(xCenter, yCenter, i)


def spectralParameterCircle(xCenter, yCenter, radius, step, end):
    for i in range(radius, end + step, step):
        drawParameterCircle(xCenter, yCenter, i)


def spectralCanonicalCircle(xCenter, yCenter, radius, step, end):
    cur_r = radius
    while cur_r <= end:
        drawCanonicalCircle(xCenter, yCenter, cur_r)
        cur_r += step
            
        
def spectralTkinterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop, canvasWindow):
    i = 0
    xi = 0
    yi = 0
    while i < stop:
        drawTkinterEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi, canvasWindow)
        i += 1
        print(i)
        xi += stepX
        yi += stepY


def spectralMiddlePointEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = 0
    yi = 0
    while i < stop:
        drawMiddlePointEllipseAlg(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        print(i)
        xi += stepX
        yi += stepY


def spectralBresenhamEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = 0
    yi = 0
    while i < stop:
        drawBresenhamEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        print(i)
        xi += stepX
        yi += stepY


def spectralParameterEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = 0
    yi = 0
    while i < stop:
        drawParameterEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        print(i)
        xi += stepX
        yi += stepY


def spectralCanonicalEllipse(xCenter, yCenter, xRadius, yRadius, stepX, stepY, stop):
    i = 0
    xi = 0
    yi = 0
    while i < stop:
        drawCanonicalEllipse(xCenter, yCenter, xRadius + xi, yRadius + yi)
        i += 1
        print(i)
        xi += stepX
        yi += stepY
        
def timeResearch(canvasWindow, option_fig):
    my_option = option_fig.get()
    if my_option == 1:
        circleTimeResearch(canvasWindow)
    else:
        ellipseTimeResearch(canvasWindow)

def circleTimeResearch(canvasWindow):
    masTime = []
    masAllTime = []
    START = 100
    RMAX = 2000
    STEP = 100
    REPS = 100
    i = START
    
    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            canonicalCircleAlg(0, 0, i, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
            
        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            parameterCircleAlg(0, 0, i, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()

        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            bresenhamCircleAlg(0, 0, i, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()

        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START


    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            middlePointCircleAlg(0, 0, i, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
            
        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START


    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            drawTkinterCircle(canvasWindow, 0, 0, i)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
            
        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)  

    fig = plt.figure(figsize = (15, 7))
    plot = fig.add_subplot()
    ran = []
    for i in range(START, RMAX + STEP, STEP):
        ran.append(i)

    plot.plot(ran, masAllTime[0], label = "Алгоритм на основе канонического уравнения")
    plot.plot(ran, masAllTime[1], label = "Алгоритм на основе параметрического уравнения")
    plot.plot(ran, masAllTime[2], label = "Алгоритм Брезенхема")
    plot.plot(ran, masAllTime[3], label = "Алгоритм средней точки")
    plot.plot(ran, masAllTime[4], label = "Алгоритм библиотечный")
    clear_canvas(canvasWindow)
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов построения окружностей")
    plt.ylabel("Затраченное время")
    plt.xlabel("Длина радиуса")
    plt.show()

    
def ellipseTimeResearch(canvasWindow):
    masTime = []
    masAllTime = []
    START = 100
    RMAX = 2000
    STEP = 100
    REPS = 100
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            canonicalEllipseAlg(0, 0, i, i + 30, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
            
        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            parameterEllipseAlg(0, 0, i, i + 30, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()
            
        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            bresenhamEllipseAlg(0, 0, i, i + 30, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()

        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)
    
    masTime = []
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            middlePointEllipseAlg(0, 0, i, i + 30, curColorLines, False)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()

        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)

    masTime = []
    i = START

    while i <= RMAX:
        curTime = 0
        for j in range(REPS):
            
            timeTempStart = datetime.now()
            drawTkinterEllipse(0, 0, i, i + 30, canvasWindow)
            timeTempEnd = datetime.now()
            
            curTime += timeTempEnd.timestamp() - timeTempStart.timestamp()

        curTime /= REPS
        masTime.append(curTime)
        i += STEP

    masAllTime.append(masTime)

    fig = plt.figure(figsize = (15, 7))
    plot = fig.add_subplot()
    ran = []
    for i in range(START, RMAX + STEP, STEP):
        ran.append(i)

    plot.plot(ran, masAllTime[0], label = "Алгоритм на основе канонического уравнения")
    plot.plot(ran, masAllTime[1], label = "Алгоритм на основе параметрического уравнения")
    plot.plot(ran, masAllTime[2], label = "Алгоритм Брезенхема")
    plot.plot(ran, masAllTime[3], label = "Алгоритм средней точки")
    plot.plot(ran, masAllTime[4], label = "Алгоритм библиотечный")
    clear_canvas(canvasWindow)
    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов построения эллипсов")
    plt.ylabel("Затраченное время")
    plt.xlabel("Длина радиуса")
    plt.show()
    

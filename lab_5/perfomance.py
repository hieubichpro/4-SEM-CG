from tkinter import *
from tkinter import colorchooser
from info import *
from time import time, sleep
from numpy import sign
from math import fabs

img = 0
curColorFigure = ((0, 0, 0), '#000000')
curColorBackground = ((255, 255, 255), '#FFFFFF')

polygons = [[]]
intersection_points = []
num_check = 0

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
    
def create_labels(window):
    coordsLabel = Label(window, text = "Координаты точки")
    coordsLabel.place(relx = 0.02, rely= 0.1)
    
    xLabel = Label(window, text = "X: ")
    xLabel.place(relx = 0.02, rely = 0.15)
    
    yLabel = Label(window, text = "Y: ")
    yLabel.place(relx = 0.15, rely = 0.15)
    
    modeLabel = Label(window, text = "Режим заполнения")
    modeLabel.place(relx = 0.02, rely = 0.68)    
    
    timeLabel = Label(window, text = "Время выполнения: ", font = "Consolas 13")
    timeLabel.place(relx = 0.3, rely = 0.96)
    
    return timeLabel

def create_table():
    table = Listbox(bg = "white", height = 17, width = 45)
    table.place(relx = 0.02, rely = 0.3)
    
    return table

def creat_radio_button():
    option = IntVar()
    option.set(2)
    
    no_delay = Radiobutton(text = "Без зажержки", variable = option, value = 1)
    no_delay.place(relx = 0.03, rely =0.72)
    
    no_delay = Radiobutton(text = "C зажержкой", variable = option, value = 2)
    no_delay.place(relx = 0.15, rely =0.72)
    
    return option

def create_canvas(window):
    canvas = Canvas(window, width=820, height=720, background='#FFFFFF')
    canvas.place(relx=0.28, rely=0)
    
    global img
    
    img = PhotoImage(width=820, height=720)
    canvas.create_image((410, 360), image=img, state='normal')
    img.put(curColorBackground[1], to=(0, 0, 820, 720))

    figure_canvas = Canvas(window, bg = curColorFigure[1], borderwidth = 5, relief = RIDGE, width = 40, height = 20)
    figure_canvas.place(relx=0.16, rely=0.03)
    
    return canvas, figure_canvas

def create_button(window, main_canvas, figure_canvas, option, table, timeLabel, new_point):
    choosefigureColor = Button(window, text = "Цвет заполнения", command= lambda: chooseFigureColor(figure_canvas))
    choosefigureColor.place(relx = 0.05, rely = 0.035, relheight=0.04)
    
    addPoint = Button(window, text = "Добавить точку", command=lambda: add_point_from_screen(new_point, table, main_canvas))
    addPoint.place(relx = 0.08, rely = 0.2)
    
    closeButton = Button(window, text = "Замкнуть", command = lambda : close_figure(main_canvas, table))
    closeButton.place(relx = 0.095, rely = 0.25)
    
    drawButton = Button(window, text = "Закрасить", command = lambda: fill_figura(main_canvas, option, timeLabel))
    drawButton.place(relx = 0.06, rely = 0.8, relheight=0.07, relwidth=0.15)
    
    clearButton = Button(window, text = "Очистить", command = lambda: clear_screen(main_canvas, table, timeLabel))
    clearButton.place(relx = 0.06, rely = 0.88, relheight=0.07, relwidth=0.15)
    
    main_canvas.bind("<1>", lambda e, f = table, g =main_canvas : add_point_click(e, f, g))

def chooseFigureColor(canvas_color_figure):
    global curColorFigure
    curColorFigure = colorchooser.askcolor()
    canvas_color_figure.config(bg = curColorFigure[1])
    
def create_entry(window):
    xEntry = Entry(window)
    xEntry.place(relx = 0.04, rely = 0.15, relwidth = 0.05)
    
    yEntry = Entry(window)
    yEntry.place(relx = 0.17, rely = 0.15, relwidth = 0.05)
    
    return [xEntry, yEntry]

def add_point_click(event, table, main_canvas):
    x = event.x
    y = event.y

    add_point(x, y, table, main_canvas)
    

def draw_line(main_canvas, beg, end):
    main_canvas.create_line(beg[0], beg[1], end[0], end[1], fill = 'black')

def add_point(x, y, table, main_canvas, finish = False):
    polygons[-1].append([x, y])
    table.insert(END, "%d. (%4d;%4d)" %(len(polygons[-1]), x, y))
    
    if len(polygons[-1]) > 1:
        beg = polygons[-1][-2]
        end = polygons[-1][-1]
        
        find_intersection(beg, end)
        
        draw_line(main_canvas, beg, end)
    
    elif len(polygons[-1]) == 1:
        img.put("#000000", (polygons[-1][0][0], polygons[-1][0][1]))
        

    
def add_point_from_screen(new_point, table, main_canvas):
    try:
        x = int(new_point[0].get())
        y = int(new_point[1].get())
    except:
        box.showerror("Ошибка", "Входные данные должны быть целыми")
        return
    
    add_point(x, y, table, main_canvas)
    
def clear_screen(main_canvas, table, timeLabel):
    main_canvas.delete("all")    
    global img
    img = PhotoImage(width=820, height=720)
    main_canvas.create_image((410, 360), image=img, state='normal')
    img.put(curColorBackground[1], to=(0, 0, 820, 720))
    
    table.delete(0, END)
    timeLabel.config(text = "Время выполнения: ")
    
    global polygons, intersection_points, num_check
    polygons = [[]]
    intersection_points = []
    num_check = 0
        
def find_intersection(begin, end):
    if begin[1] == end[1]:
        return
    
    if begin[1] > end[1]:
        begin, end = end, begin
        
    dy = 1
    cotg = (end[0] - begin[0]) / (end[1] - begin[1])
    dx = cotg
    
    xCur = begin[0]
    yCur = begin[1]
    
    while yCur < end[1]:
        intersection_points.append([int(xCur), yCur])
        yCur += dy
        xCur += dx
        
def fill(main_canvas, delay = False):
    
    septum = find_septum()
    # septum = polygons[0][0][0]
    
    for i in range(len(intersection_points)):
        if intersection_points[i][0] < septum:
            for j in range(intersection_points[i][0] + 1, septum + 1):
                invert_pixel(j, intersection_points[i][1])

        elif intersection_points[i][0] > septum:
            for j in range(intersection_points[i][0], septum, -1):
                invert_pixel(j, intersection_points[i][1])
        if delay:
            sleep(0.001)
            main_canvas.update()
        
                
def invert_pixel(x, y):
    color_pixel = img.get(x, y)

    if color_pixel == curColorBackground[0]:
        img.put(curColorFigure[1], (x, y))
    
    elif color_pixel == curColorFigure[0]:
        img.put(curColorBackground[1], (x, y))
        

def close_figure(main_canvas, table):
    if len(polygons[-1]) < 3:
        box.showerror("Ошибка", "Количество точек должно быть больше двух")
        return
    table.insert(END, "_" * 20)
    beg = polygons[-1][-1]
    end = polygons[-1][0]
    
    find_intersection(beg, end)
    draw_line(main_canvas, beg, end)
    global num_check
    num_check += 1
    
    polygons.append([])
    
def fill_figura(main_canvas, option, timeLabel):
    if not (num_check + 1 == len(polygons) and len(polygons[-1]) == 0):
        box.showerror("Ошибка", "Фигура не замкнута")
        return
    begin_time, end_time = 0, 0
    
    if option.get() == 1:
        begin_time = time()
        fill(main_canvas)
        end_time = time()
        
    elif option.get() == 2:
        begin_time = time()
        fill(main_canvas, True)
        end_time = time()
        
    timeLabel.config(text = "Время выполнения: {} с".format(round(end_time - begin_time, 4)))
        

def find_septum():
    x = 0
    count = 0
    for polygon in polygons:
        for point in polygon:
            x += point[0]
            count += 1
    
    x /= count
    
    xSeptum = polygons[0][0][0]
    minD = fabs(x - xSeptum)
    
    for polygon in polygons:
        for point in polygon:
            diff = fabs(x - point[0])
            if diff < minD:
                minD = diff
                xSeptum = point[0]
    
    return xSeptum
    
        
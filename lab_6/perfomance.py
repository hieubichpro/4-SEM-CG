from tkinter import *
from tkinter import colorchooser
from info import *
from time import time, sleep
from stack import stack_class
from numpy import sign

img = 0
curColorFigure = ((255, 0, 0), '#FF0000')
curColorBorder = ((0, 0, 0), '#000000')
curColorBackground = ((255, 255, 255), '#FFFFFF')
WIDTH_CANVAS = 820
HEIGHT_CANVAS = 720

polygons = [[]]
seed_point = []
check_num = 0

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
    
    seedPointLabel = Label(window, text = "Координаты затравочной точка")
    seedPointLabel.place(relx = 0.02, rely = 0.78)
    
    xSeedLabel = Label(window, text = "X: ")
    xSeedLabel.place(relx = 0.02, rely = 0.83)
    
    ySeedLabel = Label(window, text = "Y: ")
    ySeedLabel.place(relx = 0.11, rely = 0.83)
    
    timeLabel = Label(window, text = "Время выполнения: ", font = "Consolas 14")
    timeLabel.place(relx = 0.3, rely = 0.96)
    
    sizeLabel = Label(window, text = "820 x 720", font = "Consolas 14")
    sizeLabel.place(relx = 0.88, rely = 0.96)
    
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
    canvas = Canvas(window, width=WIDTH_CANVAS, height=HEIGHT_CANVAS, background='#FFFFFF')
    canvas.place(relx=0.32, rely=0)
    
    global img
    
    img = PhotoImage(width=WIDTH_CANVAS, height=HEIGHT_CANVAS)
    canvas.create_image((410, 360), image=img, state='normal')
    img.put(curColorBackground[1], to=(0, 0, WIDTH_CANVAS, HEIGHT_CANVAS))

    figure_canvas = Canvas(window, bg = curColorFigure[1], borderwidth = 5, relief = RIDGE, width = 30, height = 20)
    figure_canvas.place(relx=0.115, rely=0.03)
    
    border_canvas = Canvas(window, bg = curColorBorder[1],  borderwidth = 5, relief = RIDGE, width = 30, height = 20)
    border_canvas.place(relx = 0.255, rely = 0.03)
    
    return canvas, figure_canvas, border_canvas

def create_button(window, main_canvas, figure_canvas,border_canvas, option, table, timeLabel, new_point, new_seed_point):
    choosefigureColor = Button(window, text = "Цвет заполнения", command = lambda: chooseFigureColor(figure_canvas))
    choosefigureColor.place(relx = 0.028, rely = 0.035, relheight=0.04)
    
    chooseborderColor = Button(window, text = "Цвет границы", command = lambda: chooseBorderColor(border_canvas))
    chooseborderColor.place(relx = 0.18, rely = 0.035, relheight = 0.04)
    
    addPoint = Button(window, text = "Добавить точку", command = lambda: add_point_from_screen(new_point, table, main_canvas))
    addPoint.place(relx = 0.08, rely = 0.2)
    
    closeButton = Button(window, text = "Замкнуть", command = lambda : close_figure(main_canvas, table))
    closeButton.place(relx = 0.095, rely = 0.25)
    
    addSeedPoint = Button(window, text = "Добавить зат.точку", command = lambda: add_seed_point_from_screen(new_seed_point))
    addSeedPoint.place(relx = 0.19, rely = 0.825)
    
    drawButton = Button(window, text = "Закрасить", command = lambda: fill_wrapper(main_canvas,seed_point, option, timeLabel))
    drawButton.place(relx = 0.06, rely = 0.90, relheight=0.04, relwidth=0.15)
    
    clearButton = Button(window, text = "Очистить", command = lambda: clear_screen(main_canvas, table, timeLabel))
    clearButton.place(relx = 0.06, rely = 0.94, relheight=0.04, relwidth=0.15)
    
    main_canvas.bind("<1>", lambda e, f = table, g =main_canvas : add_point_click(e, f, g))
    main_canvas.bind("<B1-Motion>", lambda e, f = table, g =main_canvas : add_point_click(e, f, g))
    main_canvas.bind("<3>", lambda e : add_seed_point_click(e))

def chooseFigureColor(canvas_color_figure):
    global curColorFigure
    curColorFigure = colorchooser.askcolor()
    canvas_color_figure.config(bg = curColorFigure[1])
    
def chooseBorderColor(canvas_color_border):
    global curColorBorder
    curColorBorder = colorchooser.askcolor()    
    canvas_color_border.config(bg = curColorBorder[1])
    
def create_entry(window):
    xEntry = Entry(window)
    xEntry.place(relx = 0.04, rely = 0.15, relwidth = 0.05)
    
    yEntry = Entry(window)
    yEntry.place(relx = 0.17, rely = 0.15, relwidth = 0.05)
    
    xSeedEntry = Entry(window)
    xSeedEntry.place(relx = 0.04, rely = 0.83, relwidth = 0.03)
    xSeedEntry.insert(0, "410")

    ySeedEntry = Entry(window)
    ySeedEntry.place(relx = 0.13, rely = 0.83, relwidth = 0.03)
    ySeedEntry.insert(0, "360")
    
    return [xEntry, yEntry], [xSeedEntry, ySeedEntry]

def add_point_click(event, table, main_canvas):
    x = event.x
    y = event.y

    if not (0 <= x <= WIDTH_CANVAS) or not (0 <= y <= HEIGHT_CANVAS):
        box.showerror("Ошибка", "Выходится за границей дисплея")
        return

    add_point(x, y, table, main_canvas)
    
def add_seed_point_click(event):
    x = event.x
    y = event.y

    if not (0 <= x <= WIDTH_CANVAS) or not (0 <= y <= HEIGHT_CANVAS):
        box.showerror("Ошибка", "Выходится за границей дисплея")
        return

    add_seed_point(x, y)

def intBresenham(xStart, yStart, xEnd, yEnd):
    if xStart == xEnd and yStart == yEnd:
        img.put(curColorBorder[1], (xStart, yStart))
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

    for i in range(deltaX):
        img.put(curColorBorder[1], (curX, curY))

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

def add_point(x, y, table, main_canvas, finish = False):
    polygons[-1].append([x, y])
    table.insert(END, "%d. (%4d;%4d)" %(len(polygons[-1]), x, y))
    
    if len(polygons[-1]) > 1:
        beg = polygons[-1][-2]
        end = polygons[-1][-1]
        
        intBresenham(beg[0], beg[1], end[0], end[1])
    
    elif len(polygons[-1]) == 1:
        img.put(curColorBorder[1], (polygons[-1][0][0], polygons[-1][0][1]))
        
def add_seed_point(x, y):
    img.put(curColorFigure[1], (x, y))
    global seed_point
    seed_point = [x, y]
    
    
    
def add_point_from_screen(new_point, table, main_canvas):
    try:
        x = int(new_point[0].get())
        y = int(new_point[1].get())
    except:
        box.showerror("Ошибка", "Входные данные должны быть целыми")
        return
    
    if not (0 <= x <= WIDTH_CANVAS) or not (0 <= y <= HEIGHT_CANVAS):
        box.showerror("Ошибка", "Выходится за границей дисплея")
        return
    
    add_point(x, y, table, main_canvas)
    
def clear_screen(main_canvas, table, timeLabel):
    main_canvas.delete("all")    
    global img
    img = PhotoImage(width=WIDTH_CANVAS, height=HEIGHT_CANVAS)
    main_canvas.create_image((410, 360), image=img, state='normal')
    img.put(curColorBackground[1], to=(0, 0, WIDTH_CANVAS, HEIGHT_CANVAS))
    
    table.delete(0, END)
    timeLabel.config(text = "Время выполнения: ")
    
    global polygons, check_num
    polygons = [[]]
    check_num = 0
        

def close_figure(main_canvas, table):
    if len(polygons[-1]) < 3:
        box.showerror("Ошибка", "Количество точек должно быть больше двух")
        return
    table.insert(END, "_" * 20)
    beg = polygons[-1][-1]
    end = polygons[-1][0]
    
    intBresenham(beg[0], beg[1], end[0], end[1])
    global check_num
    check_num += 1
    polygons.append([])
    
def add_seed_point_from_screen(new_seed_point):
    try:
        x = int(new_seed_point[0].get())
        y = int(new_seed_point[1].get())
    except:
        box.showerror("Ошибка", "Входные данные должны быть целыми")
        return

    if not (0 <= x <= WIDTH_CANVAS) or not (0 <= y <= HEIGHT_CANVAS):
        box.showerror("Ошибка", "Выходится за границей дисплея")
        return
    
    add_seed_point(x, y)
    
        
def fill(main_canvas, seed_point, delay = False):
    stack = stack_class(seed_point)

    while not stack.is_empty():

        x, y = stack.pop()

        img.put(curColorFigure[1], (x, y))

        x_right = fill_right(x + 1, y)
        x_left = fill_left(x - 1, y)

        find_pixel(stack, x_right, x_left, y + 1)
        find_pixel(stack, x_right, x_left, y - 1)
        
        if delay:
            sleep(0.01)
            main_canvas.update()

def fill_right(x, y):
    while img.get(round(x), round(y)) != curColorBorder[0]:
        img.put(curColorFigure[1], (x, y))
        x += 1
        if x == WIDTH_CANVAS:
            box.showerror('Ошибка', "Затравочная находится вне области")
            return
    return x - 1

def fill_left(x, y):
    while img.get(round(x), round(y)) != curColorBorder[0]:
        img.put(curColorFigure[1], (x, y))
        x -= 1
        if x == 0:
            box.showerror('Ошибка', "Затравочная находится вне области")
            return
        
    return x + 1

def find_pixel(stack, x_right, x_left, y):
    x = x_left

    while x <= x_right:
        # Флаг - признак нахождения нового затравочного пикселя.
        flag = False
        # Пока цвет текущего пикселя не равен цвету заполнения и не равен граничному цвету и x <= x_right
        while compare_color_border(x, y) and compare_color_fill(x, y) and x <= x_right:
            # Нашли затравочный пиксель.
            if flag == False:
                flag = True
            x += 1

        # Если нашли новый пиксель, то помещаем его в стек.
        if flag:
            if x == x_right and compare_color_border(x, y) and compare_color_fill(x, y):
                stack.push([x, y])
            else:
                stack.push([x - 1, y])
            flag = False

        # Продолжаем проверку (Если интервал был прерван)
        x_temp = x
        while (not compare_color_border(x, y) or not compare_color_fill(x, y)) and x < x_right:
            x += 1
            
        # удостоверимся, что координата пиксела увеличена
        if x == x_temp:
            x += 1
            
def compare_color_border(x, y):
        return img.get(round(x), round(y)) != curColorBorder[0]

def compare_color_fill(x, y):
        return img.get(round(x), round(y)) != curColorFigure[0]
    
def fill_wrapper(main_canvas, seed_point, option, timeLabel):
    if not seed_point:
        box.showerror("Ошибка", "Пока не задана точка затравки")
        return
    if not (check_num + 1 == len(polygons) and len(polygons[-1]) == 0):
        box.showerror("Ошибка", "Фигура не замкнута")
        return
    
    begin_time, end_time = 0, 0
    
    if option.get() == 1:
        begin_time = time()
        fill(main_canvas, seed_point)
        end_time = time()
        
    elif option.get() == 2:
        begin_time = time()
        fill(main_canvas, seed_point, True)
        end_time = time()
        
    timeLabel.config(text = "Время выполнения: {} с".format(round(end_time - begin_time, 4)))
    
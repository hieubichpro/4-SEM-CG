from tkinter import *
from tkinter import messagebox, colorchooser
from math import *
import colorutils as cu
from itertools import combinations

AUTHOR = "Фам Минь Хиеу - ИУ7-42Б"
TASK = "«Реализация алгоритма отсечения отрезка произвольным выпуклым отсекателем»"

lines = [[]]
cutter = []

X_MIN = 0
X_MAX = 1
Y_MIN = 2
Y_MAX = 3

X_DOT = 0
Y_DOT = 1

color_rec = ((255, 0, 0), 0)
color_line = ((0, 255, 0), 0)
color_result = ((0, 0, 255), 0)

def change_color_rec():
    global color_rec
    color_rec = colorchooser.askcolor()
    changecolor_rec.config(bg = color_rec[1])

def change_color_line():
    global color_line
    color_line = colorchooser.askcolor()
    changecolor_line.config(bg = color_line[1])

def change_color_result():
    global color_result
    color_result = colorchooser.askcolor()
    changecolor_result.config(bg = color_result[1])

def add_line_click(event):
    x = event.x
    y = event.y

    add_line(x, y)

def add_line(x, y):
    cur_line = len(lines) - 1

    if (len(lines[cur_line]) == 0):
        lines[cur_line].append([x, y])
    else:
        lines[cur_line].append([x, y])
        lines[cur_line].append(color_line)
        lines.append(list())

        x1 = lines[cur_line][0][0]
        y1 = lines[cur_line][0][1]

        x2 = lines[cur_line][1][0]
        y2 = lines[cur_line][1][1]

        canvas.create_line(x1, y1, x2, y2, fill = cu.Color(color_line[0]).hex)

def read_dot():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return
    add_dot(int(x), int(y))

def add_dot_click(event):
    x = event.x
    y = event.y

    add_dot(x, y)

def add_line(x, y):
    cur_line = len(lines) - 1

    if (len(lines[cur_line]) == 0):
        lines[cur_line].append([x, y])
    else:
        lines[cur_line].append([x, y])
        lines[cur_line].append(color_line)
        lines.append(list())

        x1 = lines[cur_line][0][0]
        y1 = lines[cur_line][0][1]

        x2 = lines[cur_line][1][0]
        y2 = lines[cur_line][1][1]

        canvas.create_line(x1, y1, x2, y2, fill = cu.Color(color_line[0]).hex)

def read_line():
    global lines

    try:
        x1 = int(x_start_line_entry.get())
        y1 = int(y_start_line_entry.get())
        x2 = int(x_end_line_entry.get())
        y2 = int(y_end_line_entry.get())
    except:
        messagebox.showinfo("Ошибка", "Неверно введены координаты")
        return

    cur_line = len(lines) - 1

    lines[cur_line].append([x1, y1])
    lines[cur_line].append([x2, y2])
    lines[cur_line].append(color_line)

    lines.append(list())
    
    canvas.create_line(x1, y1, x2, y2, fill = cu.Color(color_line[0]).hex)

def is_maked():
    maked = False
    if (len(cutter) > 3):
        if ((cutter[0][0] == cutter[len(cutter) - 1][0]) and (cutter[0][1] == cutter[len(cutter) - 1][1])):
            maked = True

    return maked

def add_dot(x, y, last = True):
    if (is_maked()):
        cutter.clear()
        canvas.delete("all")
        draw_lines()
        dotslist_box.delete(0, END)

    cutter.append([x, y])
    cur_dot = len(cutter) - 1
    if (last):
        dotslist_box.insert(END, "%d. (%4d;%4d)" %(cur_dot + 1, x, y))

    if (len(cutter) > 1):
        canvas.create_line(cutter[cur_dot - 1], cutter[cur_dot], fill = cu.Color(color_rec[0]).hex)

def make_figure():
    cur_dot = len(cutter)

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")

    add_dot(cutter[0][0], cutter[0][1], last = False)

def draw_lines():
    for line in lines:
        if (len(line) != 0):
            x1 = line[0][0]
            y1 = line[0][1]

            x2 = line[1][0]
            y2 = line[1][1]

            color_line = line[2]
            canvas.create_line(x1, y1, x2, y2, fill = cu.Color(color_line[0]).hex)

def clear_screen():
    global lines
    global cutter
    lines = [[]]
    cutter = []
    dotslist_box.delete(0, END)
    canvas.delete("all")

def get_vector(dot1, dot2):
    return [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]

def vector_mul(vec1, vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]

def scalar_mul(vec1, vec2):
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1])

def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1*y2 - x2*y1

    return a, b, c

def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1*b2 - a2*b1
    opr1 = (-c1)*b2 - b1*(-c2)
    opr2 = a1*(-c2) - (-c1)*a2

    if (opr == 0):
        return -5, -5 

    x = opr1 / opr
    y = opr2 / opr

    return x, y

def is_coord_between(left_coord, right_coord, dot_coord):
    return (min(left_coord, right_coord) <= dot_coord) \
            and (max(left_coord, right_coord) >= dot_coord)

def is_dot_between(dot_left, dot_right, dot_intersec):
    return is_coord_between(dot_left[X_DOT], dot_right[X_DOT], dot_intersec[X_DOT]) \
            and is_coord_between(dot_left[Y_DOT], dot_right[Y_DOT], dot_intersec[Y_DOT])

def are_connected_sides(line1, line2):
    if ((line1[0][X_DOT] == line2[0][X_DOT]) and (line1[0][Y_DOT] == line2[0][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[1][X_DOT]) and (line1[1][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[0][X_DOT] == line2[1][X_DOT]) and (line1[0][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[0][X_DOT]) and (line1[1][Y_DOT] == line2[0][Y_DOT])):
        return True
    return False

# def extra_check(): 
#     cutter_lines = []
#     for i in range(len(cutter) - 1):
#         cutter_lines.append([cutter[i], cutter[i + 1]]) 
#     combs_lines = list(combinations(cutter_lines, 2)) 
#     for i in range(len(combs_lines)):
#         line1 = combs_lines[i][0]
#         line2 = combs_lines[i][1]
#         if (are_connected_sides(line1, line2)):
#             continue
#         a1, b1, c1 = line_koefs(line1[0][X_DOT], line1[0][Y_DOT], line1[1][X_DOT], line1[1][Y_DOT])
#         a2, b2, c2 = line_koefs(line2[0][X_DOT], line2[0][Y_DOT], line2[1][X_DOT], line2[1][Y_DOT])
#         dot_intersec = solve_lines_intersection(a1, b1, c1, a2, b2, c2)
#         if (is_dot_between(line1[0], line1[1], dot_intersec)) \
#                 and (is_dot_between(line2[0], line2[1], dot_intersec)):
#             return True
#     return False

def check_polygon(): 
    if (len(cutter) < 3):
        return False
    sign = 1 if (vector_mul(get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1])) > 0) else - 1
    for i in range(3, len(cutter)):
        if sign * vector_mul(get_vector(cutter[i - 1], cutter[i]), get_vector(cutter[i - 2], cutter[i - 1])) < 0:
            return False
    return True

def find_normal(dot1, dot2, dot3):
    pos_vect = get_vector(dot2, dot3)
    n = [dot2[Y_DOT] - dot1[Y_DOT], dot1[X_DOT] - dot2[X_DOT]]

    if scalar_mul(n, pos_vect) < 0:
        n = [-n[0], -n[1]]
    return n

def convert_parametric(line, t):
    return [line[0][0] + (line[1][0] - line[0][0]) * t, line[0][1] + (line[1][1] - line[0][1]) * t]

def cyrus_beck_algorithm(line, n):
    dot1 = line[0]
    dot2 = line[1]

    # Изначально считаем, что отрезок полностью видимый.
    t_bottom = 0
    t_top = 1

    # Находим директрису отрезка (Определяем направление).
    D = get_vector(dot1, dot2)
    
    # Цикл отсечения отрезка.
    for i in range(-2, n - 2):
        # Находим W (fi - верширны многоугольника).
        W = get_vector(cutter[i], dot1)
        # Находим вектор внутренней нормали.
        N = find_normal(cutter[i], cutter[i + 1], cutter[i + 2])

        D_scalar = scalar_mul(D, N)
        W_scalar = scalar_mul(W, N)

        # Если отрезок расположен параллельно i-ой стороне отсекателя
        if (D_scalar == 0):
            if (W_scalar < 0):
                return
            continue

        t = -W_scalar / D_scalar
        # Если Dск > 0 - то точку пересечения
        # нужно отнести к группе, определяющей начало видимой части.
        if (D_scalar > 0):
            
            if (t > 1):    # Если т. пересечения вне отрезка .Значит отрезок невидим.
                return
            t_bottom = max(t_bottom, t)   # Иначе нужно из точек, определяющих начало, выбрать максимальное.
            
        # Если Dск < 0 - то точку пересечения нужно отнести к
        # группе, определяющей конец видимой части.
        elif (D_scalar < 0):
            
            if (t < 0):    # Если т. пересечения вне отрезка .Значит отрезок невидим.
                return
            t_top = min(t_top, t)   # Иначе нужно из точек, определяющих конец, выбрать минимальное.  
            
        # Проверка видимости отрезка
        if (t_bottom > t_top):
            return
        
    dot1_res = convert_parametric(line, t_bottom)
    dot2_res = convert_parametric(line, t_top)
    
    canvas.create_line(dot1_res, dot2_res, fill = cu.Color(color_result[0]).hex)

def find_start_dot():
    y_max = cutter[0][Y_DOT]
    dot_index = 0

    for i in range(len(cutter)):
        if (cutter[i][Y_DOT] > y_max):
            y_max = cutter[i][Y_DOT]
            dot_index = i
    cutter.pop()
    for _ in range(dot_index):
        cutter.append(cutter.pop(0))
    cutter.append(cutter[0])
    if (cutter[-2][0] > cutter[1][0]):
        cutter.reverse()

def cut_area():
    if (not is_maked()):
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if (len(cutter) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    canvas.create_polygon(cutter, outline = cu.Color(color_rec[0]).hex, fill = "white")
    find_start_dot()
    dot = cutter.pop()
    for line in lines:
        if (line):
            cyrus_beck_algorithm(line, len(cutter))
    cutter.append(dot)

window = Tk()
window.title('Лабораторная работа 8: Реализация алгоритма отсечения отрезка произвольным выпуклым отсекателем')
window.geometry('1200x750+180+20')

window.columnconfigure(0, weight = 1)
window.columnconfigure(1, weight = 1)
window.rowconfigure(0, weight = 1)

canvas = Canvas(window, bg = 'white', width = 880, height = 720)
canvas.place(relx = 0.25, rely = 0)

canvas.bind("<3>", add_line_click)
canvas.bind("<1>", add_dot_click)

add_dot_label = Label(window, text = "Координаты точки")
add_dot_label.place(relx = 0.03, rely = 0.02)

x_text_label = Label(window, text = "X: ")
x_text_label.place(relx = 0.02, rely = 0.07)

x_entry = Entry(window)
x_entry.place(relx = 0.04, rely = 0.07, relwidth=0.07, relheight=0.03)

y_text_label = Label(window, text = "Y: ")
y_text_label.place(relx = 0.15, rely = 0.07)

y_entry = Entry(window)
y_entry.place(relx = 0.17, rely = 0.07, relwidth=0.07, relheight=0.03)

dotslist_box = Listbox(window, bg = "white")
dotslist_box.configure(height = 10, width = 40)
dotslist_box.place(relx = 0.03, rely = 0.27)

adddot_button = Button(window, text = "Добавить точку", command = lambda: read_dot())
adddot_button.place(relx = 0.08, rely = 0.13, relheight=0.06)

make_figure_button = Button(window, text = "Замкнуть отсекатель", command = lambda: make_figure())
make_figure_button.place(relx = 0.068, rely = 0.2, relheight=0.06)

cutter_text = Label(window, text = "Координаты концов отрезка")
cutter_text.place(relx = 0.03, rely = 0.515)

x_start_line_text = Label(window, text = "Нач. X: ")
x_start_line_text.place(relx = 0.02, rely = 0.56)

x_start_line_entry = Entry(window)
x_start_line_entry.place(relx = 0.06, rely = 0.56, relwidth=0.04)

y_start_line_text = Label(window, text = "Нач. Y: ")
y_start_line_text.place(relx = 0.14, rely = 0.56)

y_start_line_entry = Entry(window)
y_start_line_entry.place(relx = 0.18, rely = 0.56, relwidth=0.04)


x_end_line_text = Label(window, text = "Кон. X: ")
x_end_line_text.place(relx = 0.02, rely = 0.61)

x_end_line_entry = Entry(window)
x_end_line_entry.place(relx = 0.06, rely = 0.61, relwidth=0.04)

y_end_line_text = Label(window, text = "Кон. Y: ")
y_end_line_text.place(relx = 0.14, rely = 0.61)

y_end_line_entry = Entry(window)
y_end_line_entry.place(relx = 0.18, rely = 0.61, relwidth=0.04)


add_line_btn = Button(window, text = "Нарисовать отрезок", command = lambda: read_line())
add_line_btn.place(relx = 0.065, rely = 0.65, relheight=0.05)

changecolor_rec = Button(window, text = 'Цвет отсекателя', bg = "#ff0000", command = lambda: change_color_rec())
changecolor_rec.place(relx = 0.02, rely = 0.73, relheight=0.05)
changecolor_line = Button(window, text = 'Цвет отрезка', bg = "#00ff00", command = lambda: change_color_line())
changecolor_line.place(relx = 0.15, rely = 0.73, relheight=0.05)
changecolor_result = Button(window, text = 'Цвет результата', bg = "#0000ff", command = lambda: change_color_result())
changecolor_result.place(relx = 0.09, rely = 0.79, relheight=0.05)

cut_btn = Button(window, text = "Отсечь", command = lambda: cut_area())
cut_btn.place(relx = 0.08, rely = 0.85, relheight=0.07, relwidth=0.1)

clear_btn = Button(window, text = "Очистить экран", command = lambda: clear_screen())
clear_btn.place(relx = 0.07, rely = 0.92, relheight=0.07, relwidth=0.12)

menubar = Menu(window) 
info_menu = Menu(menubar, tearoff = 0)
info_menu.add_command(label="О авторе", command = lambda: messagebox.showinfo("О авторе", AUTHOR))
info_menu.add_command(label="О программе", command = lambda: messagebox.showinfo("О программе", TASK))
menubar.add_cascade(label="Инфор", menu = info_menu)
exit_menu = Menu(menubar, tearoff = 0)
menubar.add_command(label = "Выход", command = window.destroy)
window.config(menu = menubar)

window.mainloop()
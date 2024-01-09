from tkinter import *
from tkinter import messagebox
from math import *
from tkinter import colorchooser
from my_constant import *

AUTHOR = "Фам Минь Хиеу - ИУ7-42Б"
TASK = "Реализация алгоритма отсечения отрезка регулярным отсекателем"

def choose_color_background(canv):
    global color_bg
    color_bg = colorchooser.askcolor()
    canv.configure(bg=color_bg[1])
    ent_bg_canvas.configure(bg=color_bg[1])

def choose_color_line():
    global color_line
    color_line = colorchooser.askcolor()
    ent_line.configure(bg=color_line[1])

def choose_color_rectangle():
    global color_rectangle
    color_rectangle = colorchooser.askcolor()
    ent_rectangle.configure(bg=color_rectangle[1])

def choose_color_result():
    global color_result
    color_result = colorchooser.askcolor()
    ent_result.configure(bg=color_result[1])


# For rectangle
is_set_rect = False

def clear_canvas():
    global lines
    global rect

    canvas.delete("all")

    lines = [[]]
    rect = [-1, -1, -1, -1]


def add_rect_click1(event):
    global is_set_rect

    is_set_rect = False


def add_rect_click(event):
    global rect
    global is_set_rect

    cutter_color = color_rectangle[1]

    if (is_set_rect == False):
        rect[X_MIN] = event.x
        rect[Y_MAX] = event.y

        is_set_rect = True
    else:
        x_first = rect[X_MIN]
        y_first = rect[Y_MAX]

        x = event.x
        y = event.y

        canvas.delete("all")
        canvas.create_rectangle(x_first, y_first, x, y, outline = cutter_color)

        rect[X_MAX] = x
        rect[Y_MIN] = y

        draw_lines()

    
def add_rect():
    global rect

    try:
        x_min = int(xleft_cutter_entry.get())
        y_max = int(yleft_cutter_entry.get())
        x_max = int(xright_cutter_entry.get())
        y_min = int(yright_cutter_entry.get())
    except:
        messagebox.showinfo("Ошибка", "Неверно введены координаты")
        return

    cutter_color = color_rectangle[1]

    canvas.delete("all")
    canvas.create_rectangle(x_min, y_max, x_max, y_min, outline = cutter_color)

    rect = [x_min, x_max, y_min, y_max]

    draw_lines()


def draw_lines():

    for line in lines:
        if (len(line) != 0):
            x1 = line[0][0]
            y1 = line[0][1]

            x2 = line[1][0]
            y2 = line[1][1]

            color_line = line[2]

            canvas.create_line(x1, y1, x2, y2, fill = color_line)

def add_line_click(event):

    line_color = color_line[1]
    
    x = event.x
    y = event.y

    cur_line = len(lines) - 1

    if (len(lines[cur_line]) == 0):
        lines[cur_line].append([x, y])
    else:
        lines[cur_line].append([x, y])
        lines[cur_line].append(line_color)
        lines.append(list())

        x1 = lines[cur_line][0][0]
        y1 = lines[cur_line][0][1]

        x2 = lines[cur_line][1][0]
        y2 = lines[cur_line][1][1]

        canvas.create_line(x1, y1, x2, y2, fill = line_color)


def add_line():
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

    line_color = color_line[1]

    lines[cur_line].append([x1, y1])
    lines[cur_line].append([x2, y2])
    lines[cur_line].append(line_color)

    lines.append(list())
    
    canvas.create_line(x1, y1, x2, y2, fill = line_color)


def create_code(rect, dot):
    
    code = 0b0000

    if (dot[X_DOT] < rect[X_MIN]):
        code += 0b0001

    if (dot[X_DOT] > rect[X_MAX]):
        code += 0b0010
    
    if (dot[Y_DOT] > rect[Y_MIN]): # из-за экранной системы координат поменены
        code += 0b0100
        
    if (dot[Y_DOT] < rect[Y_MAX]):
        code += 0b1000

    return code


def check_visible(code_1, code_2):

    status = MAYBE_PARTLY_VISIBLE # частично видимый

    if (code_1 == 0 and code_2 == 0):
        status = VISIBLE # видим
        
    elif (code_1 & code_2 != 0):
        status = INVISIBLE # не видим полностью

    return status


def get_bit(code, i):
    return (code >> i) & 1


def are_bits_equal(code_1, code_2, i):
    return True if get_bit(code_1, i) == get_bit(code_2, i) else False


def sutherland_cohen(rect, line):
    
    dot1 = [line[0][X_DOT], line[0][Y_DOT]]
    dot2 = [line[1][X_DOT], line[1][Y_DOT]]

    flag = NORMAL_LINE
    m = 1

    if (dot1[X_DOT] == dot2[X_DOT]):
        flag = VERTICAL_LINE  # вертикальный
    else:
        m = (dot2[Y_DOT] - dot1[Y_DOT]) / (dot2[X_DOT] - dot1[X_DOT])

        if (m == 0):
            flag = HORIZONTAL_LINE # горизонтальный

    for i in range(4):
        code_1 = create_code(rect, dot1)
        code_2 = create_code(rect, dot2)

        vision = check_visible(code_1, code_2)

        if (vision == INVISIBLE):
            return # выйти и не рисовать
        elif (vision == VISIBLE):
            break # нарисовать и выйти

        if (are_bits_equal(code_1, code_2, i)):
            continue

        if get_bit(code_1, i) == 0:
            tmp = dot1
            dot1 = dot2
            dot2 = tmp

        if (flag != VERTICAL_LINE):
            if (i < 2):
                dot1[Y_DOT] = m * (rect[i] - dot1[X_DOT]) + dot1[Y_DOT]
                dot1[X_DOT] = rect[i]

            else:
                dot1[X_DOT] = (1 / m) * (rect[i] - dot1[Y_DOT]) + dot1[X_DOT]
                dot1[Y_DOT] = rect[i]
        else:
            dot1[Y_DOT] = rect[i]

    res_color = color_result[1]

    canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill = res_color)
            

def cut_area():
    global rect

    if (rect[0] == -1):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")

    rect = [min(rect[0], rect[1]), max(rect[0], rect[1]), max(rect[2], rect[3]), min(rect[2], rect[3])]

    canvas.create_rectangle(rect[X_MIN], rect[Y_MAX], rect[X_MAX], rect[Y_MIN], fill = color_bg[1], outline = color_rectangle[1])
    
    for line in lines:
        if (line):
            sutherland_cohen(rect, line)

if __name__ == "__main__":

    window = Tk()
    window.geometry("%dx%d+%d+%d" %(window_WIDTH, window_HEIGHT, window_LEFTMERGIN, window_TOPMERGIN))
    window.title("Лабораторная работа 7")

    menu = Menu(window)
    menu.add_command(label="Об авторе", command=lambda: messagebox.showinfo("Об авторе", AUTHOR))
    menu.add_command(label="Об программе", command=lambda: messagebox.showinfo("Об программе", TASK))
    menu.add_command(label='Выход', command=window.destroy)
    window.configure(menu=menu)

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)

    color_line = ((0, 0, 0), '#000000')
    color_bg = ((255, 255, 255), '#ffffff')
    color_rectangle = ((199, 36, 7), '#c72407')
    color_result = ((31, 192, 47), '#1fc02f')

    canvas = Canvas(window, width = CV_WIDE, height = CV_HEIGHT, bg = "white")
    canvas.grid(row = 0, column = 1, padx = 10, pady = 10)

    frame = Frame(window, width = 250, height = 750)
    frame.grid(row = 0, column = 0, padx = 10, pady = 10)

    # Binds

    lines = [[]]
    canvas.bind("<3>", add_line_click)

    rect = [-1, -1, -1, -1]
    canvas.bind("<1>", add_rect_click1)
    canvas.bind('<B1-Motion>', add_rect_click)

    button = Button(frame)
    button.configure(text="Цвет фона", command=lambda: choose_color_background(canvas))
    button.place(relx=0.07, rely=0.02, relheight=0.03, relwidth=0.45)

    button1 = Button(frame)
    button1.configure(text="Цвет отрезка", command=lambda: choose_color_line())
    button1.place(relx=0.07, rely=0.07, relheight=0.03, relwidth=0.45)

    button2 = Button(frame)
    button2.configure(text="Цвет отсекателя", command=lambda: choose_color_rectangle())
    button2.place(relx=0.07, rely=0.12, relheight=0.03, relwidth=0.45)
    
    button3 = Button(frame)
    button3.configure(text="Цвет результата", command=lambda: choose_color_result())
    button3.place(relx=0.07, rely=0.17, relheight=0.03, relwidth=0.45)

    ent_bg_canvas = Label(frame, text =" " *5, font="-family {Consolas} -size 14", bg=color_bg[1])
    ent_bg_canvas.place(relx=0.6, rely=0.02, relheight=0.03, relwidth=0.27)

    ent_line = Label(frame, text =" " *5, font="-family {Consolas} -size 14", bg=color_line[1])
    ent_line.place(relx=0.6, rely=0.07, relheight=0.03, relwidth=0.27)
    ent_line.configure(bg=color_line[1])

    ent_rectangle = Label(frame, text =" " *5, font="-family {Consolas} -size 14", bg=color_rectangle[1])
    ent_rectangle.place(relx=0.6, rely=0.12, relheight=0.03, relwidth=0.27)

    ent_result = Label(frame, text =" " *5, font="-family {Consolas} -size 14", bg=color_result[1])
    ent_result.place(relx=0.6, rely=0.17, relheight=0.03, relwidth=0.27)

    # Add cutter

    cutter_text = Label(frame, text = "Координаты отсекателя", bg = MAIN_TEXT_COLOR)
    cutter_text.place(relx=0, rely=0.22, relheight=0.03, relwidth=1)

    left_text = Label(frame, text = "Левый верхний: ", bg = TEXT_MAIN_BOX)
    left_text.place(relx=0, rely=0.26, relheight=0.03, relwidth=1)

    xleft_cutter_text = Label(frame, text = "X: ", bg = BOX_COLOR)
    xleft_cutter_text.place(relx=0.02, rely=0.30, relheight=0.03, relwidth=0.047)

    xleft_cutter_entry = Entry(frame)
    xleft_cutter_entry.place(relx=0.07, rely=0.30, relheight=0.03, relwidth=0.4)

    yleft_cutter_text = Label(frame, text = "Y: ", bg = BOX_COLOR)
    yleft_cutter_text.place(relx=0.52, rely=0.30, relheight=0.03, relwidth=0.047)

    yleft_cutter_entry = Entry(frame)
    yleft_cutter_entry.place(relx=0.57, rely=0.30, relheight=0.03, relwidth=0.4)

    right_text = Label(frame, text = "Правый нижний: ", bg = TEXT_MAIN_BOX)
    right_text.place(relx=0, rely=0.34, relheight=0.03, relwidth=1)

    xright_cutter_text = Label(frame, text = "X: ", bg = BOX_COLOR)
    xright_cutter_text.place(relx=0.02, rely=0.38, relheight=0.03, relwidth=0.047)

    xright_cutter_entry = Entry(frame)
    xright_cutter_entry.place(relx=0.07, rely=0.38, relheight=0.03, relwidth=0.4)

    yright_cutter_text = Label(frame, text = "Y: ", bg = BOX_COLOR)
    yright_cutter_text.place(relx=0.52, rely=0.38, relheight=0.03, relwidth=0.047)

    yright_cutter_entry = Entry(frame)
    yright_cutter_entry.place(relx=0.57, rely=0.38, relheight=0.03, relwidth=0.4)


    add_cutter_btn = Button(frame, text = "Нарисовать отсекатель", command = lambda: add_rect())
    add_cutter_btn.place(relx=0.08, rely=0.43, relwidth=0.81, relheight=0.06)

    # Add line
    cutter_text = Label(frame, text = "Добавить отрезок", bg = MAIN_TEXT_COLOR)
    cutter_text.place(relx=0, rely=0.52, relheight=0.03, relwidth=1)

    begin_text = Label(frame, text = "Начало:", bg = TEXT_MAIN_BOX)
    begin_text.place(relx=0, rely=0.56, relheight=0.03, relwidth=1)

    x_start_line_text = Label(frame, text = "X: ", bg = BOX_COLOR)
    x_start_line_text.place(relx=0.02, rely=0.60, relheight=0.03, relwidth=0.047)

    x_start_line_entry = Entry(frame)
    x_start_line_entry.place(relx=0.07, rely=0.60, relheight=0.03, relwidth=0.4)

    y_start_line_text = Label(frame, text = "Y: ", bg = BOX_COLOR)
    y_start_line_text.place(relx=0.52, rely=0.60, relheight=0.03, relwidth=0.047)

    y_start_line_entry = Entry(frame)
    y_start_line_entry.place(relx=0.57, rely=0.60, relheight=0.03, relwidth=0.4)

    end_text = Label(frame, text = "Конец:", bg = TEXT_MAIN_BOX)
    end_text.place(relx=0, rely=0.64, relheight=0.03, relwidth=1)

    x_end_line_text = Label(frame, text = "X: ", bg = BOX_COLOR)
    x_end_line_text.place(relx=0.02, rely=0.68, relheight=0.03, relwidth=0.047)

    x_end_line_entry = Entry(frame)
    x_end_line_entry.place(relx=0.07, rely=0.68, relheight=0.03, relwidth=0.4)

    y_end_line_text = Label(frame, text = "Y: ", bg = BOX_COLOR)
    y_end_line_text.place(relx=0.52, rely=0.68, relheight=0.03, relwidth=0.047)

    y_end_line_entry = Entry(frame)
    y_end_line_entry.place(relx=0.57, rely=0.68, relheight=0.03, relwidth=0.4)


    add_line_btn = Button(frame, text = "Нарисовать отрезок", command = lambda: add_line())
    add_line_btn.place(relx=0.08, rely=0.73, relwidth=0.81, relheight=0.06)

    cut_btn = Button(frame, text = "Отсечь", command = lambda: cut_area())
    cut_btn.place(relx=0.15, rely=0.82, relwidth=0.7, relheight=0.08)

    clear_btn = Button(frame, text = "Очистить экран", command = lambda: clear_canvas())
    clear_btn.place(relx=0.15, rely=0.91, relwidth=0.7, relheight=0.08)

    window.mainloop()
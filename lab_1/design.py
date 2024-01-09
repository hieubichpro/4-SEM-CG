from tkinter import *
import math as m
import tkinter.ttk as ttk
import message as msg
import feature as ft
import geometry as g
import tkinter.font as font

def create_labels(window):
    xLabel = Label(window, text = "X:")
    xLabel.place(relx=0.02, rely=0.46, relwidth=0.03, relheight=0.05)
    yLabel = Label(window, text = "Y:")
    yLabel.place(relx=0.13, rely=0.46, relwidth=0.03, relheight=0.05)
    ansLabel = Label(window, text = "", font = 'Consolas 12')
    ansLabel.place(relx=0.25, y = 602)
    
    return ansLabel
    
def create_menu(window):
    menubar = Menu(window)
    
    filemenu = Menu(menubar, tearoff = 0)
    filemenu.add_command(label = "Выход", command=window.destroy)
    menubar.add_cascade(label="Файл", menu=filemenu)
    
    infomenu = Menu(menubar, tearoff = 0)
    infomenu.add_command(label = "О авторе", command = msg.show_author)
    infomenu.add_command(label = "О программе", command = msg.show_task)
    menubar.add_cascade(label = "Информации", menu = infomenu)
    
    window.config(menu = menubar)

def create_table(window):
    table = ttk.Treeview(window, columns = ('#1', '#2'), selectmode = 'browse')

    table.heading('#0', text='№')
    table.heading('#1', text='X')
    table.heading('#2', text='Y')

    table.column('#0', width=40)
    table.column('#1', width=108)
    table.column('#2', width=108)

    table.place(relx=0.02, rely=0.05, relheight=0.33, relwidth=0.23)

    scr_points = ttk.Scrollbar(table, orient='vertical', command=table.yview)
    table.configure(yscrollcommand=scr_points.set)
    scr_points.pack(side='right', fill='y')
    
    return table
    

def create_buttons(window, table, entry, canvas, ansLabel):
    addBtn = Button(window, text = "Добавить точку", command = lambda: ft.add_point(table, entry))
    addBtn.place(relx=0.023, rely=0.529, relwidth=0.2, relheight=0.05)
    
    deleteBtn = Button(window, text = "Удалить точку", command = lambda: ft.del_point(table))
    deleteBtn.place(relx=0.023, rely=0.589, relwidth=0.2, relheight=0.05)
    
    solveBtn = Button(window, text = "Найти", command = lambda: ft.solve(table, canvas, ansLabel))
    solveBtn.place(relx=0.023, rely=0.805, relwidth=0.2, relheight=0.05)
    
    cleanBtn = Button(window, text = "Очистить", command = lambda: ft.clean(table, entry, canvas, ansLabel))
    cleanBtn.place(relx=0.023, rely=0.865, relwidth=0.2, relheight=0.05)
    
    editBtn = Button(window)
    applyBtn = Button(window)

    buttons = [addBtn, deleteBtn, solveBtn, cleanBtn, editBtn]
    
    editBtn.place(relx=0.023, rely=0.649, relwidth=0.2, relheight=0.05)
    editBtn.configure(text = "Редактировать точку", command = lambda: ft.edit_point(table, entry, buttons, applyBtn))

    applyBtn.configure(state = DISABLED, text = "Применить", command = lambda: ft.apply(table, entry, buttons, applyBtn))
    applyBtn.place(relx=0.023, rely=0.709, relwidth=0.2, relheight=0.085)
    
    
def create_entry(window):
    xEntry = Entry(window)
    xEntry.place(relx=0.015, rely=0.44, relwidth=0.1, relheight=0.03)
    
    yEntry = Entry(window)
    yEntry.place(relx=0.135, rely=0.44, relwidth=0.1, relheight=0.03)
    
    return [xEntry, yEntry]

def create_canvas(window):
    canvas = Canvas(window, width = 900, height=600, background="white")
    canvas.place(relx=0.245, y=0)
    return canvas

def create_point(canvas, limits, point, name, index):
    x, y = new_coords(canvas, limits, point)
    size = 2.5
    canvas.create_oval(x-size, y+size, 
                       x+size, y-size, fill='red')
    canvas.create_text(x, y - size * 5, 
                       text = "%s%d(%.2f,%.2f)" %(name, index + 1, point[0],point[1]),
                        font = ("Courier New", 8, "bold"), fill = "darkmagenta")

def draw_line(canvas,limits, A, B, color, dsh):
    xA,yA = new_coords(canvas, limits, A)
    xB, yB = new_coords(canvas, limits, B)
    canvas.create_line(xA, yA,xB, yB,
                       fill = color, width = 1.5, dash=dsh)


def build_triangle(cv, points,indexes,limits):
    H = g.find_H(points[0], points[1], points[2])
    M = g.find_M(points[1], points[2])
    x1 = points[0][0] + 0.25 * (H[0] - points[0][0])
    y1 = points[0][1] + 0.25 * (H[1] - points[0][1])
    x2 = points[0][0] + 0.25 * ((points[1][0] + points[2][0]) / 2 - points[0][0])
    y2 = points[0][1] + 0.25 * ((points[1][1] + points[2][1]) / 2 - points[0][1])
    x3,y3 = new_coords(cv, limits, [x1, y1])
    x4,y4 = new_coords(cv, limits, [x2, y2])
    angle = m.acos(g.get_cosin(points[0], points[1], points[2]))*180/(m.pi)
    
    for i in range(3): 
        create_point(cv, limits, points[i], "A", indexes[i])
    create_point(cv, limits, H, "H", indexes[0])
    create_point(cv, limits, M, "M", indexes[0])
    draw_line(cv, limits, points[0], H, "red",None)
    draw_line(cv, limits, points[0], M, "green",None)
    draw_line(cv, limits, [x1,y1], [x2,y2],"black", None)
    cv.create_text((x3 + x4) / 2, -20 + (y3 + y4) / 2, text="{:.2f}°".format(angle), justify=CENTER, font="Ubuntu 10")
    
    draw_line(cv, limits, points[0], points[1], "blue",None)
    draw_line(cv, limits, points[1], points[2], "blue",None)
    draw_line(cv, limits, points[2], points[0], "blue",None)

    draw_line(cv, limits, points[1], H, "blue",(10,5))

def new_coords(canvas,limits, point):
    mergin = 50
    width, height = canvas.winfo_reqwidth()-4, canvas.winfo_reqheight()-4
    if limits[0] == limits[1]:
        limits[1] += 1
    if limits[2] == limits[3]:
        limits[3] += 1
    one = min((width -mergin * 2)/(limits[1] - limits[0]), (height - mergin * 2)/(limits[3] - limits[2]))
    
    center = [(limits[1] + limits[0]) / 2, (limits[3] + limits[2]) / 2]
    
    x = width/2 + one * (point[0] - center[0])
    y = height/2 - one * (point[1] - center[1])
    
    return [x, y]
    
    
def on_line_case(canvas, ansLabel, points):
    
    limits = ft.find_limit(points)
    
    for i in range(len(points)):
        create_point(canvas, limits, points[i], "A", i)
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            A, B = points[i], points[j]
            draw_line(canvas, limits, A, B, "blue", None)
            
    ansLabel.config(text = "Вырожденный случай!\nВсе точки лежат на одной прямой")
    
def normal_case(canvas, ansLabel, points, res):
    all_points = []
    for index in res:
        A, B, C = points[index[0]], points[index[1]], points[index[2]]
        H, M = g.find_H(A, B, C), g.find_M(B, C)
        all_points.extend([A, B, C, H, M])
    
    limits = ft.find_limit(all_points)
    
    ans = "Результирующий треугольник построен на точках: \n"
    
    for index in res:
        A, B, C = points[index[0]], points[index[1]], points[index[2]]
        angle = m.acos(g.get_cosin(A, B, C))*180/(m.pi)
        build_triangle(canvas, [A, B, C], index, limits)
        ans += "A%d(%.2f,%.2f), A%d(%.2f,%.2f), A%d(%.2f,%.2f).Угол равен %.2f в вершине A%d(%.2f,%.2f)\n"%(index[0]+1, A[0], A[1], index[1]+1, B[0], B[1], index[2]+1, C[0], C[1], angle, index[0]+1, A[0], A[1])
    ansLabel.config(text = ans)
    

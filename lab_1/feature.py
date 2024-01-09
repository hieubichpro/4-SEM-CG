import math as m
import tkinter as tk
import tkinter.messagebox as box
import geometry as g
import design as ds


def update_after_delete(table):
    for i, point in enumerate(table.get_children()):
        table.item(point, text = i + 1)


def create_arr(table):
    points = []
    for child in table.get_children():
        points.append([float(x) for x in table.item(child)["values"]])
    
    return points

def clean(table, entry, canvas, ansLabel):
    table.delete(*table.get_children())
    entry[0].delete(0, 'end')
    entry[1].delete(0, 'end')
    canvas.delete('all')
    ansLabel.config(text = "")

def apply(table, entry, buttons, applyBtn):
    try:
        x = float(entry[0].get())
        y = float(entry[1].get())
        
        selected_point = table.selection()[0]
        table.item(selected_point, values=("{:.2f}".format(x), "{:.2f}".format(y)))
        
        entry[0].delete(0, 'end')
        entry[1].delete(0, 'end')
        
        for button in buttons:
            button.configure(state = tk.NORMAL)
        
        applyBtn.configure(state = tk.DISABLED)
        table.configure(selectmode = 'browse')
        
    except ValueError:
        if not entry[0].get() or not entry[1].get():
            box.showerror("Ошибка", "Пустой ввод")
        else:
            box.showerror("Ошибка", "Данные должны быть числами")

def find_limit(points):
    xLeft, xRight = None, None
    yLeft, yRight = None, None
    for point in points:
        if xLeft is None and xRight is None:
            xLeft, xRight = point[0], point[0]
        if point[0] < xLeft:
            xLeft = point[0]
        if point[0] > xRight:
            xRight = point[0]
            
        if yLeft is None and yRight is None:
            yLeft, yRight = point[1], point[1]
        if point[1] < yLeft:
            yLeft = point[1]
        if point[1] > yRight:
            yRight = point[1]
    return [m.floor(xLeft), m.ceil(xRight), m.floor(yLeft), m.ceil(yRight)]
        
        
def solve(table, canvas, ansLabel):
    points = create_arr(table)
    if not points:
        box.showerror("Ошибка", "Нет никаких точек")
        return
    if len(points) < 3:
        box.showerror("Ошибка", "Количество точек должны больше двух")
        return
    canvas.delete('all')
    res = g.findTriangle(points)
    print(res)
    if not res:
        ds.on_line_case(canvas, ansLabel, points)
    else:
        ds.normal_case(canvas, ansLabel, points, res)

def add_point(table, entry):
    try:
        x = float(entry[0].get())
        y = float(entry[1].get())
        
    except ValueError:
        if not entry[0].get() or not entry[1].get():
            box.showerror("Ошибка", "Пустой ввод")
        else:
            box.showerror("Ошибка", "Данные должны быть числами")
    else:
        idx = len(table.get_children('')) + 1
        table.insert('', tk.END, text = idx, values=("{:.2f}".format(x), "{:.2f}".format(y)))

def del_point(table):
    try:
        table.delete(table.selection()[0])
        update_after_delete(table)
    except:
        if not table.get_children():
            box.showerror("Ошибка", "Нет никаках точек")
        else:
            box.showerror("Ошибка", "Точка не выбрана")

def edit_point(table, entry, buttons, applyBtn):
    try:
        selected_item = table.selection()[0]
        point = table.item(selected_item)["values"]

        entry[0].delete(0, 'end')
        entry[1].delete(0, 'end')
        
        entry[0].insert(0, point[0])
        entry[1].insert(0, point[1])
        
        for button in buttons:
            button.configure(state = tk.DISABLED)

        applyBtn.configure(state = tk.NORMAL)
        table.configure(selectmode = 'none')
    except:
        if not table.get_children():
            box.showerror("Ошибка", "Нет никаках точек")
        else:
            box.showerror("Ошибка", "Точка не выбрана")



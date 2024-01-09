from functions import *
from tkinter import *
from fish import *
import tkinter.messagebox as box
from copy import deepcopy

def move_figura(canvas, storage, entry, xy_center_label, preBtn):
    fish_points = deepcopy(storage[-1])
    coefs = [0] * 2
    try:
        coefs[0] = float(entry[0].get())
        coefs[1] = float(entry[1].get())
        
        for part in fish_points:
            for point in part:
                move_point(point, coefs)
        
        draw_fish(canvas, fish_points)
        add_to_storage(storage, fish_points)
        config_label(xy_center_label, fish_points[0][0])
        preBtn.configure(state=NORMAL)
    except:
        if not entry[0].get() or not entry[1].get():
            box.showerror("Ошибка", "Пустой ввод")
        else:
            box.showerror("Ошибка", "dx, dy должны быть числами")

def scale_figura(canvas, storage, entry, xy_center_label, preBtn):
    fish_points = deepcopy(storage[-1])
    center = [0] * 2
    coefs = [0] * 2
    try:
        center[0] = float(entry[0].get())
        center[1] = float(entry[1].get())
    
        coefs[0] = float(entry[2].get())
        coefs[1] = float(entry[3].get())
    
        for part in fish_points:
            for point in part:
                scale_point(point, center, coefs)
        
        draw_fish(canvas, fish_points)
        add_to_storage(storage, fish_points)
        config_label(xy_center_label, fish_points[0][0])
        preBtn.configure(state=NORMAL)
    except:
        for et in entry:
            if not et.get():
                box.showerror("Ошибка", "Пустой ввод")
                return
        
        box.showerror("Ошибка", "Некорректные данные\nКоэффициенты и координаты должны быть числами")
    
def rotate_figura(canvas, storage, entry, xy_center_label, preBtn):
    fish_points = deepcopy(storage[-1])
    center = [0] * 2
    try:
        center[0] = float(entry[0].get())
        center[1] = float(entry[1].get())
        
        alpha = float(entry[2].get())
        
        for part in fish_points:
            for point in part:
                rotate_point(point, center, alpha)
        
        draw_fish(canvas, fish_points)
        add_to_storage(storage, fish_points)
        config_label(xy_center_label, fish_points[0][0])
        preBtn.configure(state=NORMAL)
    except:
        for et in entry:
            if not et.get():
                box.showerror("Ошибка", "Пустой ввод")
                return
        box.showerror("Ошибка", "Некорректные данные\nУгол и координаты должны быть числами")
    
def original_figura(canvas, storage, xy_center_label, preBtn):
    storage.clear()
    fish_points = create_fish()
    storage.append(fish_points)
    draw_fish(canvas, fish_points)
    preBtn.configure(state=DISABLED)
    config_label(xy_center_label, fish_points[0][0])
    
def undo_action(canvas, storage, xy_center_label, preBtn):
    sub_from_storage(storage)
    fish_points = storage[-1]
    draw_fish(canvas, fish_points)
    config_label(xy_center_label, fish_points[0][0])
    if len(storage) == 1:
        preBtn.configure(state = DISABLED)
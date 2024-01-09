from tkinter import *
from message import *
from feature import *
from fish import *

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
    centerFiguraLabel = Label(window, text='Центр Фигуры')
    centerFiguraLabel.place(relx=0.025, rely=0.02)
    
    xyFiguraLabel = Label(window, text = "X = 0.00   , Y = 0.00    ")
    xyFiguraLabel.place(relx=0.06, rely=0.06)
    
    moveLabel = Label(window, text='Перенос')
    moveLabel.place(relx=0.025, rely=0.14)
    
    dxLabel = Label(window, text='dx:')
    dxLabel.place(relx=0.028, rely=0.18)
    
    dyLabel = Label(window, text='dy:')
    dyLabel.place(relx=0.12, rely=0.18)
    
    centerTransformLabel = Label(window, text='Центр преобразований')
    centerTransformLabel.place(relx=0.025, rely = 0.35)
    
    xCenterTransformLabel = Label(window, text='Xc:')
    xCenterTransformLabel.place(relx=0.028, rely=0.39)
    
    yCenterTransformLabel = Label(window, text='Yc:')
    yCenterTransformLabel.place(relx=0.12, rely=0.39)
    
    resizeLabel = Label(window, text='Масштабирование')
    resizeLabel.place(relx=0.028, rely=0.47)
    
    xResizeLabel = Label(window, text='Kx')
    xResizeLabel.place(relx=0.028, rely=0.52)
    
    yResizeLabel = Label(window, text='Ky')
    yResizeLabel.place(relx=0.12, rely=0.52)
    
    spinLabel = Label(window, text='Поворот')
    spinLabel.place(relx=0.025, rely=0.66)
    
    spinAngelLabel = Label(window, text='Угол(°)')
    spinAngelLabel.place(relx=0.028, rely=0.7)
    
    return xyFiguraLabel
    
def create_button(window, canvas, entry, xy_center_label):
    storage = []
    storage.append(create_fish())
    
    preBtn = Button(window, text='Назад',state=DISABLED)
    preBtn.place(relx=0.015, rely=0.83, relwidth=0.18, relheight=0.06)
    preBtn.configure(command = lambda: undo_action(canvas, storage, xy_center_label, preBtn))
    
    moveBtn = Button(window, text='Перенести', command = lambda: move_figura(canvas, storage, entry[0], xy_center_label, preBtn))
    moveBtn.place(relx=0.015, rely=0.23, relwidth=0.18, relheight=0.05)
    
    resizeBtn = Button(window, text = "Масштабировать", command = lambda :scale_figura(canvas, storage, entry[1], xy_center_label, preBtn))
    resizeBtn.place(relx=0.015, rely=0.57, relwidth=0.18, relheight=0.05)
    
    spinBtn = Button(window, text='Повернуть', command = lambda: rotate_figura(canvas, storage, entry[2], xy_center_label, preBtn))
    spinBtn.place(relx=0.015, rely=0.75, relwidth=0.18, relheight=0.05)
    
    originalBtn = Button(window, text='Исходный рисунок', command = lambda: original_figura(canvas, storage, xy_center_label, preBtn))
    originalBtn.place(relx=0.015, rely=0.9, relwidth=0.18, relheight=0.08)
    
def create_entry(window):
    dxEntry = Entry(window)
    dxEntry.place(relx=0.05, rely=0.18, relwidth=0.06, relheight=0.04)
    
    dyEntry = Entry(window)
    dyEntry.place(relx=0.14, rely=0.18, relwidth=0.06, relheight=0.04)
    
    xCenterTransformEntry = Entry(window)
    xCenterTransformEntry.place(relx=0.05, rely=0.39, relwidth=0.06, relheight=0.04)
    
    yCenterTransformEntry = Entry(window)
    yCenterTransformEntry.place(relx=0.14, rely=0.39, relwidth=0.06, relheight=0.04)
    
    xResizeEntry = Entry(window)
    xResizeEntry.place(relx=0.05, rely=0.52, relwidth=0.06, relheight=0.04)
    
    yResizeEntry = Entry(window)
    yResizeEntry.place(relx=0.14, rely=0.52, relwidth=0.06, relheight=0.04)
    
    angleEntry = Entry(window)
    angleEntry.place(relx=0.08, rely=0.7, relwidth=0.08, relheight=0.04)
    return [[dxEntry, dyEntry], [xCenterTransformEntry, yCenterTransformEntry, xResizeEntry, yResizeEntry], [xCenterTransformEntry, yCenterTransformEntry, angleEntry]]

def create_canvas(window):
    canvas = Canvas(window, width=960, height=720, background='white')
    canvas.place(relx=0.24, rely=0)
    draw_fish(canvas, create_fish())
    return canvas
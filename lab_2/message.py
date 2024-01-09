import tkinter.messagebox as box

AUTHOR = "Фам Минь Хиеу - ИУ7-42Б"
TASK = "Нарисовать исходный рисунок, осуществить его перенос, поворот, масштабирование"

def about_author():
    box.showinfo("Info", AUTHOR)

def about_task():
    box.showinfo("Info", TASK)
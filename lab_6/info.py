import tkinter.messagebox as box

AUTHOR = "Фам Минь Хиеу - ИУ7-42Б"
TASK = "РЕАЛИЗАЦИЯ И ИССЛЕДОВАНИЕ АЛГОРИТМА ПОСТРОЧНОГО ЗАТРАВОЧНОГО  ЗАПОЛНЕНИЯ СПЛОШНЫХ ОБЛАСТЕЙ"

def about_author():
    box.showinfo("Info", AUTHOR)

def about_task():
    box.showinfo("Info", TASK)
import tkinter.messagebox as box

AUTHOR = "Фам Минь Хиеу - ИУ7-42Б"
TASK = "На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках\nу которого угол, образованный высотой и медианой, исходящий из одной вершины, минимален"

def show_author():
    box.showinfo("Info", AUTHOR)
    
def show_task():
    box.showinfo("Info", TASK)
from tkinter import *
from design import *
from feature import *

window = Tk()
window.title("Лабораторная работа 1: Геометрия")
window.geometry('1200x750+150+15')
window.minsize(500, 500)

create_menu(window)
ansLabel = create_labels(window)
points = create_table(window)
entry = create_entry(window)
canvas = create_canvas(window)
create_buttons(window, points, entry, canvas, ansLabel)

window.mainloop()
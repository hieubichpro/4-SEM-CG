from tkinter import *
from message import *
from feature import *
from design import *
from fish import *

WIDTH = 1280
HEIGHT = 730
LEFT_MERGIN = 150
RIGHT_MERGIN = 15

window = Tk()
window.title("Лабораторная работа 2: Преобразование")
window.geometry("%dx%d+%d+%d"%(WIDTH, HEIGHT, LEFT_MERGIN, RIGHT_MERGIN))

create_menu(window)
xy_center_label = create_label(window)
canvas = create_canvas(window)
entry = create_entry(window)
create_button(window, canvas, entry, xy_center_label)

window.mainloop()
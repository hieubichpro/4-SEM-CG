from tkinter import *
from performance import *

WIDTH, HEIGHT = 1270, 730
LEFT_MERGIN, TOP_MERGIN = 120, 30

window = Tk()
window.title("Лабораторная работа 3: Построение отрезков")
window.geometry("%dx%d+%d+%d"%(WIDTH, HEIGHT, LEFT_MERGIN, TOP_MERGIN))

create_menu(window)
create_label(window)
list_box = create_listbox(window)
all_entry =  create_entry(window)
main_canvas, line_canvas, bg_canvas = create_canvas(window)
create_button(window, main_canvas, line_canvas, bg_canvas, all_entry, list_box)

window.mainloop()
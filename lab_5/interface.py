from tkinter import *
from perfomance import *

WIDTH = 1150
HEIGHT = 758
LEFT_MERGIN = 190
TOP_MERGIN = 2

window = Tk()
window.title("Лабораторная работа 5: Алгоритм заполнения по рёбрам с перегородкой")
window.geometry("%dx%d+%d+%d"%(WIDTH, HEIGHT, LEFT_MERGIN, TOP_MERGIN))

create_menu(window)
timeLabel = create_labels(window)
table = create_table()
option = creat_radio_button()
new_point = create_entry(window)
main_canvas, figura_canvas = create_canvas(window)
create_button(window, main_canvas, figura_canvas, option, table, timeLabel, new_point)
window.mainloop()
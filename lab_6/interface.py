from tkinter import *
from perfomance import *

WIDTH = 1220
HEIGHT = 758
LEFT_MERGIN = 190
TOP_MERGIN = 2

window = Tk()
window.title("Лабораторная работа 6: Алгоритм построчного затравочного заполнения сплошных областей")
window.geometry("%dx%d+%d+%d"%(WIDTH, HEIGHT, LEFT_MERGIN, TOP_MERGIN))

create_menu(window)
timeLabel = create_labels(window)
table = create_table()
option = creat_radio_button()
new_point, new_seed_point = create_entry(window)
main_canvas, figura_canvas, border_canvas = create_canvas(window)
create_button(window, main_canvas, figura_canvas, border_canvas, option, table, timeLabel, new_point, new_seed_point)
window.mainloop()
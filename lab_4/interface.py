from tkinter import *
from design import *

WIDTH, HEIGHT = 1270, 730
LEFT_MERGIN, TOP_MERGIN = 120, 30

window = Tk()
window.title("Лабораторная работа 4: Построение окружностей, эллипсов")
window.geometry("%dx%d+%d+%d"%(WIDTH, HEIGHT, LEFT_MERGIN, TOP_MERGIN))

create_menu(window)
label =  create_label(window)
all_entry =  create_entry(window)
list_box = create_listbox(window)
option, hidden_spekt = create_radioButton(label, all_entry)
main_canvas, line_canvas, bg_canvas = create_canvas(window)
create_button(window, main_canvas, line_canvas, bg_canvas, all_entry, list_box, option, hidden_spekt)

window.mainloop()
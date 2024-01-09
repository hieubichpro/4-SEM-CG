from tkinter import NORMAL, DISABLED, Label
from math import fabs

def change_figure(option, label, entry, hidden_button):
    R_label, R_a_label, R_b_label = label[0]
    r_start, r_end, step_circle, quantity_circle, hidden_label = label[1]
    r_a, r_b, step_a, step_b, quantity_ellipse = label[2]
    
    r_circle, r_a_ellipse, r_b_ellipse = entry[1]
    step_r, N_circle, R_beg, R_end = entry[3]
    step_R_a, step_R_b, R_a, R_b, N_ellipse = entry[4]
    
    r_beg_hidden, r_end_hidden, quantity_hidden, step_hidden = hidden_button
    
    if option.get() == 1:
        R_a_label.place_forget()
        R_b_label.place_forget()
        r_a.place_forget()
        r_b.place_forget()
        step_a.place_forget()
        step_b.place_forget()
        quantity_ellipse.place_forget()
        
        r_a_ellipse.place_forget()
        r_b_ellipse.place_forget()
        step_R_a.place_forget()
        step_R_b.place_forget()
        R_a.place_forget()
        R_b.place_forget()
        N_ellipse.place_forget()
        
        R_label.place(relx = 0.12, rely = 0.27)
        r_start.place(relx = 0.02, rely = 0.55)
        r_end.place(relx = 0.10, rely = 0.55)
        step_circle.place(relx = 0.18, rely = 0.55)
        quantity_circle.place(relx = 0.26, rely = 0.55)
        hidden_label.place(relx = 0.03, rely = 0.60)
        
        r_circle.place(relx = 0.14, rely = 0.27, relwidth=0.04)
        step_r.place(relx = 0.21, rely = 0.55, relwidth=0.04)
        N_circle.place(relx = 0.28, rely = 0.55, relwidth=0.04)
        R_beg.place(relx = 0.05, rely = 0.55, relwidth=0.04)
        R_end.place(relx = 0.13, rely = 0.55, relwidth=0.04)
        
        r_beg_hidden.place(relx = 0.03, rely =0.63)
        r_end_hidden.place(relx = 0.1, rely =0.63)
        quantity_hidden.place(relx = 0.17, rely =0.63)
        step_hidden.place(relx = 0.24, rely =0.63)
    else:
        R_label.place_forget()
        r_start.place_forget()
        r_end.place_forget()
        step_circle.place_forget()
        quantity_circle.place_forget()
        hidden_label.place_forget()
        
        r_circle.place_forget()
        step_r.place_forget()
        N_circle.place_forget()
        R_beg.place_forget()
        R_end.place_forget()
        
        r_beg_hidden.place_forget()
        r_end_hidden.place_forget()
        quantity_hidden.place_forget()
        step_hidden.place_forget()
        
        
        R_a_label.place(relx = 0.04, rely = 0.27)
        R_b_label.place(relx = 0.2, rely = 0.27)
        r_a.place(relx = 0.08, rely = 0.55)
        r_b.place(relx = 0.21, rely = 0.55)
        step_a.place(relx = 0.08, rely = 0.61)
        step_b.place(relx = 0.21, rely = 0.61)
        quantity_ellipse.place(relx = 0.10, rely = 0.65)
        
        r_a_ellipse.place(relx = 0.08, rely = 0.27, relwidth = 0.04)
        r_b_ellipse.place(relx = 0.24, rely = 0.27, relwidth = 0.04)
        
        R_a.place(relx = 0.12, rely = 0.55, relwidth = 0.04)
        R_b.place(relx = 0.25, rely = 0.55, relwidth = 0.04)
        step_R_a.place(relx = 0.12, rely = 0.61, relwidth = 0.04)
        step_R_b.place(relx = 0.25, rely = 0.61, relwidth = 0.04)
        N_ellipse.place(relx = 0.165, rely = 0.65, relwidth = 0.04)
        
def change_option(option, entry):
    step, quantity, r_start, r_end= entry[3]
    r_start.configure(state = NORMAL)
    r_end.configure(state = NORMAL)
    quantity.configure(state = NORMAL)
    step.configure(state = NORMAL)

    if (option.get() == 1):
        r_start.configure(state = DISABLED)
    elif (option.get() == 2):
        r_end.configure(state = DISABLED)
    elif (option.get() == 3):
        quantity.configure(state = DISABLED)
    else:
        step.configure(state = DISABLED)

def make_label(window, text_label, pos_x, pos_y):
    my_label = Label(window, text = text_label)
    my_label.place(relx = pos_x, rely=pos_y)

def to_screen_coord(my_canvas, x, y):
    width = my_canvas.winfo_reqwidth() - 4
    height = my_canvas.winfo_reqheight() - 4
    return int(x + width / 2), int(-y + height / 2)

def my_round(number):
    ret = int(number)
    if number < 0:
        if fabs(number) - abs(ret) >= 0.5:
            return ret - 1
        else:
            return ret
    else:
        if number - ret >= 0.5:
            return ret + 1
        else:
            return ret

def draw_center(canvas):
    w = canvas.winfo_reqwidth() - 4
    h = canvas.winfo_reqheight() - 4
    
    canvas.create_oval(w/2-1.5, h/2+1.5, 
                       w/2+1.5, h/2-1.5, fill='red')
    
    canvas.create_text(w/2, h/2 - 2 * 5, 
                       text = "%s(%d,%d)" %("O", 0,0),
                        font = ("Courier New", 8, "bold"), fill = "darkmagenta")
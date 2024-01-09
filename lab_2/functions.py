from math import *

def to_radians(alpha):
    return alpha * pi / 180

def to_screen_coord(canvas, point):
    w, h = canvas.winfo_reqwidth()-4, canvas.winfo_reqheight()-4
    return [point[0] + w/2, -point[1] + h/2]

def add_to_storage(storage, new_points):
    storage.append(new_points)

def sub_from_storage(storage):
    storage.pop()
    
def config_label(label, new_center):
    label.configure(text = "X = {:.2f}     Y = {:.2f}".format(new_center[0], new_center[1]))

def move_point(point, coefs):
    point[0] += coefs[0]
    point[1] += coefs[1]
    
def scale(point, coefs):
    point[0] *= coefs[0]
    point[1] *= coefs[1]
    
def scale_point(point, center, coefs):
    move_to_center(point, center)
    scale(point, coefs)
    move_back(point, center)

def move_to_center(point, center):
    coefs = [-center[0], -center[1]]
    move_point(point, coefs)
    
def move_back(point, center):
    move_point(point, center)
    
def rotate(point, alpha):
    tmp_x = point[0]
    point[0] = point[0] * cos(to_radians(alpha)) - point[1] * sin(to_radians(alpha))
    point[1] = tmp_x * sin(to_radians(alpha)) + point[1] * cos(to_radians(alpha))
    
def rotate_point(point, center, alpha):
    move_to_center(point, center)
    rotate(point, alpha)
    move_back(point, center)
    

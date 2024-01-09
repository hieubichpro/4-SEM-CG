
from feature import *
from functions import *

def create_fish():
    body = []
    head = []
    eye = []
    center = [0, 0]

    for i in range(0, 3600, 1):
        body.append([100 * cos(to_radians(i/10)), 50 * sin(to_radians(i/10))])

    for j in range(-900, 900, 1):
        head.append([- 80 + 25 * cos(to_radians(j/10)), 30 * sin(to_radians(j/10))])
    
    for k in range(0, 3600, 1):
        eye.append([-80 + 4 * cos(to_radians(k/10)), 18 + 4 * sin(to_radians(k/10))])
        
    A = [100 * cos(to_radians(115)), 50 * sin(to_radians(115))]
    B = [A[0] + 18, A[1] + 25]
    C = [B[0] + 60, B[1]]
    D = [100 * cos(to_radians(80)), 50 * sin(to_radians(80))]
    body_1 = [A, B, C, D]

    E = [100 * cos(to_radians(15)), 50 * sin(to_radians(15))]
    F = [E[0] + 20, E[1] + 20]
    G = [F[0] + 20, F[1] - 1]
    H = [E[0] + 18, E[1]]
    I = [H[0] + 20, H[1] - 25]
    K = [E[0], -E[1]]
    tail = [E,F,G,H,I,K]
    
    M = [100 * cos(to_radians(-50)), 50 * sin(to_radians(-50))]
    N = [M[0] + 15, M[1]-25]
    P = [N[0] - 110, N[1]]
    Q = [-M[0], M[1]]
    body_2 = [M, N, P, Q]
    
    X = [-85, -5]
    Y = [-75, -5]
    mouth = [X, Y]
    return [[center] ,body, body_1, body_2, tail, head, eye, mouth]
    
def draw_fish(canvas, fish_points):
    canvas.delete('all')
    w = canvas.winfo_reqwidth() - 4
    h = canvas.winfo_reqheight() - 4
    
    canvas.create_oval(w/2-2.5, h/2+2.5, 
                       w/2+2.5, h/2-2.5, fill='red')
    
    canvas.create_text(w/2, h/2 - 2.5 * 5, 
                       text = "%s(%d,%d)" %("O", 0,0),
                        font = ("Courier New", 8, "bold"), fill = "darkmagenta")
    
    
    center = to_screen_coord(canvas, fish_points[0][0])
    canvas.create_oval(center[0]-2.5, center[1]+2.5, center[0]+2.5, center[1]-2.5, fill='red')
    for i in range(33):
        canvas.create_line(30 * i, 0, 30 * i, h)
    for i in range(25):
        canvas.create_line(0, 30 *i, w, 30 * i)
    
    for part in fish_points:
        for j in range(len(part) - 1):
            p1 = to_screen_coord(canvas, part[j])
            p2 = to_screen_coord(canvas, part[j+1])
            canvas.create_line(p1, p2, width = 2)
    

    
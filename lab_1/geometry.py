import math as m

def find_M(A, B):
    xm = (A[0] + B[0]) / 2
    ym = (A[1] + B[1]) / 2
    return [xm, ym]

def get_length(A, B):
    return m.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

def find_H(A, B, C):
    xa, ya = A
    xb, yb = B
    xc, yc = C
    u = xc - xb
    v = yc - yb
    M = u**2 + v**2
    N = u*(xa - xb) + v*(ya - yb)
    t = N / M
    return [u*t + xb, v*t + yb]

def get_cosin(A, B, C):
    H = find_H(A, B, C)
    M = find_M(B, C)
    AH = get_length(A, H)
    AM = get_length(A, M)
    return AH/AM


def checkPoint(A, B, C):
    eps = 1e-9
    AB = get_length(A, B)
    AC = get_length(A, C)
    BC = get_length(B, C)
    if m.fabs(AB + AC - BC) < eps or m.fabs(AB + BC - AC) < eps or m.fabs(AC + BC - AB) < eps:
        return False
    else:
        return True

def findTriangle(points):
    eps = 1e-9
    max_cos = None
    for i in range(len(points)):
        for j in range(len(points)):
            if j == i:
                continue
            for k in range(j + 1, len(points)):
                if k == i:
                    continue
                A, B, C = points[i], points[j], points[k]
                if checkPoint(A, B, C):
                    cos_HAM = get_cosin(A, B, C)
                        
                    if max_cos is None:
                        max_cos = cos_HAM
                        
                    if cos_HAM > max_cos:
                        max_cos = cos_HAM
    print(max_cos)                   
    if max_cos is None:
        return []
    
    ans = []       
                        
    for i in range(len(points)):
        for j in range(len(points)):
            if j == i:
                continue
            for k in range(j + 1, len(points)):
                if k == i:
                    continue
                A, B, C = points[i], points[j], points[k]
                if checkPoint(A, B, C):
                    if m.fabs(get_cosin(A, B, C) - max_cos) < eps:
                        ans.append([i, j, k])
    return ans;
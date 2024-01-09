from copy import deepcopy

def Scalar(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def GetVector(line):
    return [line[1][0] - line[0][0], line[1][1] - line[0][1]]

def FindNormal(peak1, peak2, peak3):
    n = [peak2[1] - peak1[1], peak1[0] - peak2[0]]

    if Scalar([peak3[0] - peak2[0], peak3[1] - peak2[1]], n) < 0:
        n = [-n[0], -n[1]]
    return n

def IsVisiable(point, peak1, peak2, peak3):
    n = FindNormal(peak1, peak2, peak3)
    
    if Scalar(n, GetVector([peak2, point])) < 0:
        return False
    
    return True

def ConvertParametric(line, t):
    return [round(line[0][0] + (line[1][0] - line[0][0]) * t), round(line[0][1] + (line[1][1] - line[0][1]) * t)]

def FindDirection(line):
    return [line[1][0] - line[0][0], line[1][1] - line[0][1]]


def Find_W(p1, p2):
    return [p1[0] - p2[0], p1[1] - p2[1]]

def IsIntersection(ed1, ed2, peak):
    # ed1 - ребро отсекаемого многоугольника.
    # ed2 - ребро отсекателя.
    # peak - след. вершина отсекателя, нужна для
    # корректного определения нормали
    
    # Определяем видимость вершин относительно рассматриваемого ребра.
    visiable1 = IsVisiable(ed1[0], ed2[0], ed2[1], peak)
    visiable2 = IsVisiable(ed1[1], ed2[0], ed2[1], peak)
    # Если одна вершина видна, а вторая нет (Есть пересечение).
    # Иначе пересечения нет.
    if not (visiable1 ^ visiable2):
        return False
    # Ищем пересечение
    N = FindNormal(ed2[0], ed2[1], peak)
    D = FindDirection(ed1)
    W = Find_W(ed1[0], ed2[0])
    # Скалярное произведение D на N.
    DScalar = Scalar(D, N)
    # Скалярное произведение W на N.
    WScalar = Scalar(W, N)
    # DScalar может быть равен нулю в двух случаях:
    # 1. Если ребро многоугольника вырождается в точку
    # Т.е. p1 == p2. В интерфейсе обработан данный случай
    # (Пользователь не может ввести ребро у которого начало и конец совпадают)
    # 2. Если текущее ребро отсекаемого многоугольника параллельно
    # Ребру отсекателя. Такие ребра не дойдут до этого момента -
    # Они будут обработаны выше. Т.к. в этом случае нет пересечения
    # Обе вершины отсекаемого многоугольника будут либо по видимую сторону
    # Отсекателя, либо по невидимую.
    
    t = -WScalar/DScalar
    
    return ConvertParametric(ed1, t)

def SutherlandHodgman(cutter, polygon):
    # Для удобства работы алгоритма первая вершина
    # отсекателя заносится в массив дважды (В начало и конец).
    # Т.к. последнее ребро отсекателя образуется
    # последней и первой вершинами многоугольника.
    cutter.append(cutter[0])
    # Также, т.к. для поиска нормали для ребра i и i+1
    # Мне нужна вершина i+2.
    cutter.append(cutter[1])
    # Цикл по вершинам отсекателя.
    for i in range(len(cutter) - 2):
        new = []  # новый массив вершин
        # Особым образом нужно обрабатывать первую
        # точку многоугольника: для нее требуется определить
        # только видимость. Если точка видима, то она заносится
        # В результирующий список и становится начальной точкой первого ребра.
        # Если же она невидима, то она просто становится начальной точкой ребра
        # И в результирующий список не заносится.
        f = polygon[0]  # Запоминаем первую вершину.
        if IsVisiable(f,  cutter[i], cutter[i + 1], cutter[i + 2]):
            new.append(f)
        s = polygon[0]
        # Цикл по вершинам многоугольника
        for j in range(1, len(polygon)):
            # Определяем пересечение текущего ребра отсекателя (cutter[i], cutter[i + 1])
            # И рассматриваемого ребра отсекаемого многоугольника (s, polygon[j]),
            # Где s = polygon[j - 1]. cutter[i + 2] нам нужно, чтобы корректно найти нормаль.
            t = IsIntersection([s, polygon[j]], [cutter[i], cutter[i + 1]], cutter[i + 2])
            # Если есть пересечение, то заносим его в новый массив вершин.
            if t:
                new.append(t)
            # Запоминаем в s текущую вершину. (Чтобы на следующем шаге
            # Искать пересечение polygon[j - 1] и polygon[j])
            s = polygon[j]
            # Проверяем, видна ли текущая вершина
            if IsVisiable(s, cutter[i], cutter[i + 1], cutter[i + 2]):
                # Если видна, то заносим ее в новый массив вершин.
                new.append(s)
        # Если массив пуст, значит многоугольник невидимый.
        if not len(new):
            return
        t = IsIntersection([s, f], [cutter[i], cutter[i + 1]], cutter[i + 2])
        if t:
            new.append(t)
        polygon = deepcopy(new)
    return polygon
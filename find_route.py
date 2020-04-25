from math import sqrt
from math import degrees
from math import atan


def get_vector(point1, point2):
    a = (point1[1] - point2[1]) / (point1[0] - point2[0])
    smaller = min(point1, point2, key=lambda item: item[0])
    b = ((-a) * smaller[0]) + smaller[1]
    vector = [a, b]
    return vector


def get_collision(vector1, vector2):
    x = (vector2[1] - vector1[1]) / (vector1[0] - vector2[0])
    y = vector1[0] * x + vector1[1]
    collision = [x, y]
    return collision


def distance(point1, point2):
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return dist


def check_collision(point1, point2, start, end):
    collision = []
    res = False
    if point1[0] == point2[0]:
        if min(start[0], end[0]) <= point1[0] <= max(start[0], end[0]):
            collision = point1[0] * get_vector(start, end)[0] + get_vector(start, end)[1]
            res = True
    elif start[0] == end[0]:
        if min(point1[0], point2[0]) <= start[0] <= max(point1[0], point2[0]):
            collision = start[0] * get_vector(point1, point2)[0] + get_vector(point1, point2)[1]
            res = True
    elif start[0] == end[0] == point1[0] == point2[0]:
        if closer_to_end(closer_to_end(point1, point2, end), start, end) != start:
            if distance(point1, start) < distance(start, end) or distance(point2, start) < distance(start, end):
                collision = closer_to_end(point1, point2, end)
                res = True
    else:
        vector = get_vector(point1, point2)
        start_end_vector = get_vector(start, end)
        if vector[0] - start_end_vector[0] == 0:
            if vector[1] - start_end_vector[1] == 0:
                if closer_to_end(closer_to_end(point1, point2, end), start, end) != start:
                    if distance(point1, start) < distance(start, end) or distance(point2, start) < distance(start, end):
                        collision = closer_to_end(point1, point2, end)
                        res = True
        else:
            collision = get_collision(start_end_vector, vector)
            if min(start[0], end[0]) < collision[0] < max(start[0], end[0]):
                if min(point1[0], point2[0]) <= collision[0] <= max(point1[0], point2[0]):
                    if min(start[1], end[1]) < collision[1] < max(start[1], end[1]):
                        if min(point1[1], point2[1]) <= collision[1] <= max(point1[1], point2[1]):
                            res = True
    if res is False:
        collision = []
    return collision


def closer_to_end(point1, point2, end):
    dist1 = distance(point1, end)
    dist2 = distance(point2, end)
    if dist1 > dist2:
        closer = point2
    else:
        closer = point1
    return closer


def get_angel(p0, point):
    if point[0] == p0[0] and point[1] > p0[1]:
        angel = 90
    elif point[0] == p0[0] and point[1] < p0[1]:
        angel = 270
    elif point[1] == p0[1] and point[0] > p0[0]:
        angel = 0
    elif point[1] == p0[1] and point[0] < p0[0]:
        angel = 180
    else:
        if point[0] > p0[0] and point[1] > p0[1]:
            angel = degrees(atan((point[1] - p0[1]) / (point[0] - p0[0])))
        elif point[0] < p0[0] and point[1] > p0[1]:
            angel = 180 + degrees(atan((point[1] - p0[1]) / (point[0] - p0[0])))
        elif point[0] < p0[0] and point[1] < p0[1]:
            angel = 270 + degrees(atan((point[1] - p0[1]) / (point[0] - p0[0])))
        else:
            angel = 360 + degrees(atan((point[1] - p0[1]) / (point[0] - p0[0])))
    return angel


def get_point(item, edge):
    if edge == item[-1]:
        point1 = item[0]
    else:
        point1 = item[item.index(edge) + 1]
    return point1


def min_angel(item, edge, start):
    point1 = get_point(item, edge)
    point2 = item[item.index(edge) - 1]
    res = min(get_angel(start, point1), get_angel(start, point2))
    return res


def max_angel(item, edge, start):
    if edge == item[-1]:
        point1 = item[0]
    else:
        point1 = item[item.index(edge) + 1]
    point2 = item[item.index(edge) - 1]
    res = max(get_angel(start, point1), get_angel(start, point2))
    return res


def find_route(start, end, konvex_hulls):
    path = [start]
    while start != end:
        arg = False
        s_e_angel = get_angel(start, end)
        for item in konvex_hulls:
            for edge in item:
                if start == edge:
                    if max_angel(item, edge, start) - min_angel(item, edge, start) < 180:
                        if min_angel(item, edge, start) <= s_e_angel <= max_angel(item, edge, start):
                            next_point = closer_to_end(get_point(item, edge), item[item.index(edge) - 1], end)
                            path.append(next_point)
                            start = next_point
                            arg = True
                            break
                    else:
                        if min_angel(item, edge, start) >= s_e_angel or s_e_angel >= max_angel(item, edge, start):
                            next_point = closer_to_end(get_point(item, edge), item[item.index(edge) - 1], end)
                            path.append(next_point)
                            start = next_point
                            arg = True
                            break
        if arg is True:
            continue
        collisions = []
        collisions_dict = {}
        for item in konvex_hulls:
            for edge in item:
                if edge == item[-1]:
                    collision = check_collision(edge, item[0], start, end)
                else:
                    collision = check_collision(edge, item[item.index(edge) + 1], start, end)
                if collision:
                    collisions.append(collision)
                    collisions_dict[item.index(edge), konvex_hulls.index(item)] = collision
        if collisions:
            closest = min(collisions, key=lambda point: sqrt((point[0] - start[0]) ** 2 + (point[1] - start[1]) ** 2))
            path.append(closest)
            c_p = []
            for key, value in collisions_dict.items():
                if value == closest:
                    c_p = key
            if c_p[0] == konvex_hulls[c_p[1]].index(konvex_hulls[c_p[1]][-1]):
                next_point = closer_to_end(konvex_hulls[c_p[1]][c_p[0]], konvex_hulls[c_p[1]][0], end)
            else:
                next_point = closer_to_end(konvex_hulls[c_p[1]][c_p[0]], konvex_hulls[c_p[1]][(c_p[0]) + 1], end)
            path.append(next_point)
            start = next_point
        else:
            start = end
            path.append(end)
    return path

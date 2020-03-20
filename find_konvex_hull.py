from math import atan
from math import sqrt
from math import degrees


def find_lowest(obstacle):
    p0 = obstacle[0]
    for point in obstacle:
        if point[1] < p0[1]:
            p0 = point
        elif point[1] == p0[1]:
            if point[0] < p0[0]:
                p0 = point
    return p0


def distance(point, p0):
    dist = sqrt((point[0] - p0[0]) ^ 2 + (point[1] - p0[1]) ^ 2)
    return dist


def angel_from_p0(point, p0):
    if point[0] == p0[0]:
        angel = 90
    elif point[1] == p0[1] and point[0] > p0[0]:
        angel = 0
    elif point[1] == p0[1] and point[0] < p0[0]:
        angel = 180
    else:
        if point[0] - p0[0] > 0:
            angel = degrees(atan((point[1] - p0[1]) / (point[0] - p0[0])))
        else:
            angel = 180 + degrees(atan((point[1] - p0[1]) / (point[0] - p0[0])))
    return angel


def sort_by_angel(obstacle, p0):
    non_konvex_hull = [p0]
    for point in obstacle:
        arg = True
        angel = angel_from_p0(point, p0)
        if point == p0:
            continue
        for edge in non_konvex_hull:
            if edge == p0:
                continue
            if angel < angel_from_p0(edge, p0):
                non_konvex_hull.insert(non_konvex_hull.index(edge), point)
                arg = False
                break
            elif angel == angel_from_p0(edge, p0):
                if distance(point, p0) > distance(edge, p0):
                    non_konvex_hull.insert(non_konvex_hull.index(edge), point)
                    non_konvex_hull.remove(edge)
                    arg = False
                    break
        if arg is True:
            non_konvex_hull.append(point)
    return non_konvex_hull


def find_konvex_hull(non_konvex):
    for obstacle in non_konvex:
        konvex_hull = []
        p0 = find_lowest(obstacle)
        konvex_hull.append(p0)
        non_konvex_hull = sort_by_angel(obstacle, p0)
        return non_konvex_hull

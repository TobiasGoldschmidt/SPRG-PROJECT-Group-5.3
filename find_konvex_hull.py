def find_lowest(obstacle):
    p0 = obstacle[0]
    for point in obstacle:
        if point[1] < p0[1]:
            p0 = point
        elif point[1] == p0[1]:
            if point[0] < p0[0]:
                p0 = point
    return p0


def find_konvex_hull(non_konvex):
    for obstacle in non_konvex:
        konvex_hull = []
        p0 = find_lowest(obstacle)
        konvex_hull.append(p0)
    return

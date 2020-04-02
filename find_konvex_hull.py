from math import atan
from math import sqrt
from math import degrees


def find_lowest(obstacle):
    # Funkcia na hladanie najnizsieho, pripadne najnizsieho a najlavejsieho bodu.
    # Vstup je pole bodov v rovine, kazdy bod je zadany polom v tvare [x,y].
    p0 = obstacle[0]
    for point in obstacle:
        if point[1] < p0[1]:
            p0 = point
        elif point[1] == p0[1]:
            if point[0] < p0[0]:
                p0 = point
    return p0


def distance(point1, point2):
    # Funkcia na najdenie vzdialenosti dvoch bodov v rovine pomocou pytagorovej vety.
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return dist


def angel_from_p0(point, p0):
    # Funkcia na najdenie uhlu od pociatocneho bodu.
    # So stupnami pracujeme pre zjednodusenie podminenokovania.
    # Je potrebne vymedzit pripady pre ktore funkcia atan nieje definovana resp dava 2 rozne vysledky.
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
    # Funkcia ktora zoradi pole bodov podla uhlu od pociatocneho bodu.
    # Vstup je pole bodov, kazdy bod je zadany polom v tvare [x,y], a pociatocny bod, tiez v tvare [x,y].
    # Ak mame dva body s rovnakym uhlom voci pociatocnemu bodu vylucime ten blizsi k pociatocnemu bodu.
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


def vector(a, b):
    # Funkcia ktora zisti smernicu priamky prechdzajucej dvoma bodmi.
    result = (b[1] - a[1]) / (b[0] - a[0])
    return result


def left_right(p, c, n, p0):
    # Funkcia ktora zistuje ci lezi bod vpravo alebo vlavo od spojnice dvoch bodov
    # na zaklade premietnutia suradnic bodu do smernice priamky prechadzajucej tymito bodmi.
    result = False
    x = [n[0] + (c[1] - n[1]) / vector(n, p), c[1]]
    y = [c[0], n[1] + (c[0] - n[0]) * vector(n, p)]
    if (distance(c, p0) > distance(x, p0)) or (distance(c, p0) > distance(y, p0)):
        result = True
    return result


def find_konvex_hull(non_konvex):
    # Riadica funkcia tohot skriptu.
    # Vrati nekonvexny plast vsetkych utvarov.
    # Prebieha aj kontrola ci je mozne vytvorit konvexny obal utvaru.
    # Najskor najdeme najnizssi bod kazdeho utvaru, potom zoradime body podla uhlov voci nemu,
    # potom prechdzame vsetky body ci zvieraju konvexny uhol s predchzajucimi dvoma bodmi, ak nie,
    # vyradime posledny bod ktory sme zaradili do konvexneho plasta a opakujeme az kym nezviera
    # bod s dvoma poslendymi bodmi konvexny uhol.
    all_konvex_hulls = []
    for obstacle in non_konvex:
        konvex_hull = []
        p0 = find_lowest(obstacle)
        konvex_hull.append(p0)
        if len(sort_by_angel(obstacle, p0)) < 3:
            print("Objekt", non_konvex.index(obstacle), "nemá konvexný obal.")
            continue
        non_konvex_hull = sort_by_angel(obstacle, p0)[3:]
        konvex_hull.extend([sort_by_angel(obstacle, p0)[1], sort_by_angel(obstacle, p0)[2]])
        for point in non_konvex_hull:
            arg = False
            while arg is False:
                if left_right(konvex_hull[-2], konvex_hull[-1], point, p0) is True:
                    konvex_hull.append(point)
                    arg = True
                else:
                    konvex_hull.pop(-1)
                    arg = False
        all_konvex_hulls.append(konvex_hull)
    return all_konvex_hulls

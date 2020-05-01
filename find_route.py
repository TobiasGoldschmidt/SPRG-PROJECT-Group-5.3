from math import sqrt
from math import degrees
from math import atan
# Importujeme potrebne funkcie


def get_vector(point1, point2):
    # Funkcia pomocou ktorej dostaneme rovnicu priamky reprezentujucu usecku,
    # vychadza z toho ze zapis priamky v rovine je v tvare y=ax+b
    # a je smernica a b je posun
    a = (point1[1] - point2[1]) / (point1[0] - point2[0])
    smaller = min(point1, point2, key=lambda item: item[0])
    b = ((-a) * smaller[0]) + smaller[1]
    vector = [a, b]
    return vector


def get_collision(vector1, vector2):
    # Funkcia ktora nam vrati prienik dvoch priamok reprezenrujucih usecky
    # Aby sme dostali x-ovu suradnicu predelime rozdiel ich posunov rozdielom ich smernic,
    # tento vztah dostaneme ak upravime rovnost a1x+b1=a2x+b2,
    # y-ovu dopocitame z x-ovej
    x = (vector2[1] - vector1[1]) / (vector1[0] - vector2[0])
    y = vector1[0] * x + vector1[1]
    collision = [x, y]
    return collision


def distance(point1, point2):
    # Funkcia ktora nam vrati vzdialenost dvoch bodov vdaka pytagorovej vete
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return dist


def check_collision(point1, point2, start, end):
    # Funkcia ktora zisti ci prienik dvoch priamok nastal, a vrati ho ako vysledok, na useckach ktore reprezentuju,
    # bolo potrebne opodmienkovat vsetky speciale pripady, tj. jedna usecka je ovnobezna s osou y,
    # obe su rovnobezne s osou y a priamky na ktorych sa nachadzaju su totozne
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
    # Funkcia ktora zisti ktory z dvoch bodov je blizsie k tretiemu bodu,
    # pouzivame na zistenie ktory bod je blizsie k cielu cesty
    dist1 = distance(point1, end)
    dist2 = distance(point2, end)
    if dist1 > dist2:
        closer = point2
    else:
        closer = point1
    return closer


def get_angel(p0, point):
    # Funkcia ktora nam vrati uhol od pociatocneho bodu(chapeme tak za pociatocny bod je pociatok suradnicovej sustavy
    # a teda ide o uhol od osi x tejto suradnicovej sustavy,
    # so stupnami pracujeme pre zjednodusenie predstavenia si ako funguje,
    # je potrebne opodmienkovat pripady pre ktore nieje funkcia atan definovana resp dava dva rozne vysledky
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
    # Funkcia ktora vrati nasledujuceho suseda daneho vrcholu v objekte v smere hodinovych ruciciek
    if edge == item[-1]:
        point1 = item[0]
    else:
        point1 = item[item.index(edge) + 1]
    return point1


def min_angel(item, edge, start):
    # Funkcia ktora nam vrati mensi z dvoch uhlov od bodu(vysvetlenie uhol k bodu viz. comment ku funkcii get angel)
    point1 = get_point(item, edge)
    point2 = item[item.index(edge) - 1]
    res = min(get_angel(start, point1), get_angel(start, point2))
    return res


def max_angel(item, edge, start):
    # Funkcia ktora nam vrati vacsi z dvoch uhlov od bodu(vysvetlenie uhol k bodu viz. comment ku funkcii get angel)
    if edge == item[-1]:
        point1 = item[0]
    else:
        point1 = item[item.index(edge) + 1]
    point2 = item[item.index(edge) - 1]
    res = max(get_angel(start, point1), get_angel(start, point2))
    return res


def check_looping(path, konvex_hulls):
    # Funkcia ktora overi ci nevstupuje porgram do slucky, ak ano vrati spat posledny krok a zvoli ine pokracovanie
    new_path = path
    if path.count(path[-1]) > 1:
        for item2 in konvex_hulls:
            for edge2 in item2:
                if path[-1] == edge2:
                    loop = edge2
                    for item in konvex_hulls:
                        for edge in item:
                            if path[-2] == edge:
                                if item[item.index(path[-2])] == item[-1]:
                                    a = item[0]
                                    b = item[item.index(path[-2]) - 1]
                                    if loop == a:
                                        new_path.pop(-1)
                                        new_path.append(b)
                                    elif loop == b:
                                        new_path.pop(-1)
                                        new_path.append(a)
                                else:
                                    a = item[item.index(path[-2]) + 1]
                                    b = item[item.index(path[-2]) - 1]
                                    if loop == a:
                                        new_path.pop(-1)
                                        new_path.append(b)
                                    elif loop == b:
                                        new_path.pop(-1)
                                        new_path.append(a)
                                    break
                            else:
                                if edge2 == item2[-1]:
                                    a = item2[0]
                                    b = item2[item2.index(path[-2]) - 1]
                                else:
                                    a = item2[item2.index(path[-2]) + 1]
                                    b = item2[item2.index(path[-2]) - 1]
                                vector1 = get_vector(edge2, a)
                                vector2 = get_vector(edge2, b)
                                if path[-2][1] == vector1[0] * path[-2][0] + vector1[1]:
                                    new_path.pop(-1)
                                    new_path.append(a)
                                elif path[-2][1] == vector2[0] * path[-2][0] + vector2[1]:
                                    new_path.pop(-1)
                                    new_path.append(b)
                        else:
                            continue
                        break
    return new_path


def find_route(start, end, konvex_hulls):
    # Riadiaca funkcia tohoto skriptu, vrati cestu zo startu do ciela pomedzi objekty ako list suradnic
    # Najskor skontroluje ci je pozicia v ktorej sa robot momentalne nachdza vrchol nejakeho objektu, ak je zisti ci
    # cesta nesmeruje cez objekt, ak ano tak vyberie susediaci vrchol a posunie sa do neho, ak nieje vo vrchole resp.
    # je a jeho cesta nevedie cez objekt postupuje priamo smerom k cielu, ak narazi na na prekayku zastavi sa a
    # pokracuje do toho z vrcholov strany ktory je blizsie k cielu a opakuje to pokial nieje jeho momentalna pozicia
    # zhodna s cielovou poziciou
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
                            path = check_looping(path, konvex_hulls)
                            start = path[-1]
                            break
                    else:
                        if min_angel(item, edge, start) >= s_e_angel or s_e_angel >= max_angel(item, edge, start):
                            next_point = closer_to_end(get_point(item, edge), item[item.index(edge) - 1], end)
                            path.append(next_point)
                            start = next_point
                            arg = True
                            path = check_looping(path, konvex_hulls)
                            start = path[-1]
                            break
            else:
                continue
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
            # Najskor najdeme vsetky objekty do ktorych mohol narazit a z nich vyberieme najblizsi naraz
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
            path = check_looping(path, konvex_hulls)
            start = path[-1]
        else:
            start = end
            path.append(end)
    return path

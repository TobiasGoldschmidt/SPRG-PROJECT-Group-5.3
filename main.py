import json
import find_konvex_hull
import find_route
import matplotlib.pyplot as plt
# Importujeme potrebne moduly


def get_map_data():
    # Funkce, ktera nacita data a prevadi na list
    positions = []
    for i in json.load(open('map_data_1.json', 'r'))['object']:
        coordinates = i['coordinates']
        positions.append(coordinates)
    return positions


def get_path():
    # Funkce ktera nacita data o vsech testovanych cestach a prevadi je na list
    data = json.load(open('test_path.json', 'r'))['path']
    paths = []
    for i in data:
        positions = []
        positions.extend([i['start'], i['end']])
        paths.append(positions)
    return paths


def obstacles_graph(plan):
    # Funkce na vytvoreni grafu z objektu, ktere jsme dostali pomoci Grahamova algoritmu
    graph_x = []
    graph_y = []
    for obstacle in plan:
        x_coordinates = []
        y_coordinates = []
        for i in obstacle:
            x = i[0]
            y = i[1]
            x_coordinates.append(x)
            y_coordinates.append(y)
        x_coordinates.append(x_coordinates[0])
        y_coordinates.append(y_coordinates[0])
        graph_x.append(x_coordinates)
        graph_y.append(y_coordinates)
        # Pocatecni souradnice pridavame, abychom ziskali uzavreny tvar
    for i in range(len(plan)):
        plt.plot(graph_x[i - 1], graph_y[i - 1], 'black')


def graph_route(path):
    # Funkce na vyneseni cesty do grafu
    x_coordinates = []
    y_coordinates = []
    for item in path:
        x = item[0]
        y = item[1]
        x_coordinates.append(x)
        y_coordinates.append(y)
    plt.plot(x_coordinates, y_coordinates, 'r', marker='o', markerfacecolor='r', markersize=4)


def main():
    # Ridici funkce celeho programu, nejprve nacita velikost mapy,
    # pote zkontroluje, jestli jeden zadany vrchol patri více vrcholum,
    # jestlize nepatri zavola funkce z ostatnich skriptu a vykresli graf.
    # Po spusteni programu je potrebne zatvorit okno s vykreslenym grafom pre vykreslenie dalsieho grafu cesty
    check = []
    mapsize = json.load(open('map_data_1.json', 'r'))['map_size']
    for item in get_map_data():
        for i in item:
            check.append(i)
    for item in get_map_data():
        for i in item:
            if check.count(i) > item.count(i):
                print('Není možné pokračovat, jeden bod sa vyskytuje ve více objektech.')
                break
        else:
            continue
        break
    else:
        plan = find_konvex_hull.find_konvex_hull(get_map_data())
        for i in range(len(get_path())):
            path = find_route.find_route(get_path()[i][0], get_path()[i][1], plan)
            obstacles_graph(plan)
            graph_route(path)
            plt.xlim(0, mapsize[0])
            plt.ylim(0, mapsize[1])
            plt.title('Path ' + str(i + 1))
            plt.show()


if __name__ == '__main__':
    main()

import json
import find_konvex_hull.py
import find_route.py


def get_map_data():
    positions = []
    for i in json.load(open('map_data_1.json', 'r'))['object']:
        coordinates = i['coordinates']
        positions.append(coordinates)
    return positions


def get_path():
    data = json.load(open('test_path.json', 'r'))['path']
    paths = []
    for i in data:
        positions = []
        positions.extend([i['start'], i['end']])
        paths.append(positions)
    return paths


def main():
    check = []
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
            print(find_route.find_route(get_path()[i - 1][0], get_path()[i - 1][1], plan))


if __name__ == '__main__':
    main()

import json
import find_konvex_hull
import find_route


def get_map_data():
    positions = []
    for i in json.load(open('map_data_0.json', 'r'))['object']:
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
    route = []
    for item in get_map_data():
        for i in item:
            check.append(i)
    for item in get_map_data():
        for i in item:
            if check.count(i) > item.count(i):
                print('Není možné pokračovat, jeden bod se vykytuje ve více objektech.')
                break
            else:
                route = find_route.find_route(find_konvex_hull.find_konvex_hull(get_map_data()))
        else:
            continue
        break
    return route


print(main())

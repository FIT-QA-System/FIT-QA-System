import json
from pprint import pprint


def getCategory():
    with open('qas.json') as data_file:
        data = json.load(data_file)

    # pprint(data[:2])

    category = []

    for d in data:
        if d['category'] not in category:
            category.append(d['category'])

    return category

if __name__ == "__main__":
    getCategory()

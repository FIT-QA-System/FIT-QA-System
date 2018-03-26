import demjson
import json
import re

# https://grimhacker.com/2016/04/24/loading-dirty-json-with-python/
def load_dirty_json(dirty_json):
    regex_replace = [(r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json

if __name__ == "__main__":
    str_json = "{'name': 'George M. Skurla Hall', 'number': '460', 'code': '460SKU', 'description': 'George M. Skurla Hall', 'street': '180 West University Boulevard', 'city': 'MELBOURNE', 'state': 'FL', 'zip': '32901', 'latitude': '28.064472', 'longitude': '-80.624573'}"

    json_obj = load_dirty_json(str_json)

    print(json_obj['name'])
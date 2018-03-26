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

import demjson
import json
import re
from .models import *


# https://grimhacker.com/2016/04/24/loading-dirty-json-with-python/
def load_dirty_json(dirty_json):
    regex_replace = [(r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json

#TODO department, person, class, building

def get_all_entities():
    buildings = Building.objects.all()
    courses = Course.objects.all()
    departments = Department.objects.all()
    employees = Employee.objects.all()

    with open("FIT_dictionary.txt", "w") as f:
        for b in buildings:
            f.writelines(b.building_name + "\n")
            f.writelines(b.building_code + "\n")
            f.writelines(b.building_abbr + "\n")
        for c in courses:
            f.writelines(c.title + "\n")
            f.writelines(c.crn + "\n")
            f.writelines(c.subject + c.course_number + "\n")
        for d in departments:
            f.writelines(d.department_id + "\n")
            f.writelines(d.name + "\n")
        for e in employees:
            f.writelines(e.first_name + " " + e.last_name + "\n")
            f.writelines(e.last_name + "\n")

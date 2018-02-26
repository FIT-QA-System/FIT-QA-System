import json
from django.utils import timezone


with open('./QA/data/buildings.json', 'r') as f:
    data = json.load(f)

    buildings = data['records']

    for b in buildings:
        building = Building(city=b['city'],
                            state=b['state'],
                            street=b['street'],
                            zip = b['zip'],
                            building_code=b['code'],
                            building_description=b['description'],
                            building_name=b['name'],
                            building_number=b['number'],
                            building_abbr=b['code'][-3:],
                            latitude = b['latitude'] ,
                            longitude= b['longitude'],
                            update_date=timezone.now())
        building.save()
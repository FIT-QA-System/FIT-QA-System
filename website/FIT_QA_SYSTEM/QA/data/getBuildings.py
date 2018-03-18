import json
from django.utils import timezone
from QA.models import *


def buildings():
    with open('./QA/data/buildings.json', 'r') as f:
        data = json.load(f)

    buildings = data['records']

    for b in buildings:
        building = Building(city=b['city'],
                            state=b['state'],
                            street=b['street'],
                            zip=b['zip'],
                            building_code=b['code'],
                            building_description=b['description'],
                            building_name=b['name'],
                            building_number=b['number'],
                            building_abbr=b['code'][-3:],
                            latitude=b['latitude'],
                            longitude=b['longitude'],
                            update_date=timezone.now())
        building.save()

def courses(year):
    with open('./QA/data/course_spring2018.json', 'r') as f:
        data = json.load(f)

    courses = data['records']

    year = 2018

    for c in courses:

        course = Course(crn=c['crn'],
                            subject=c['subject'],
                            course_number=c['course_number'],
                            section=c['section'],
                            title=c['title'],
                            term=c['term'],
                            year=2018,
                            description=c['description'],
                            description_prereqs=c['description_with_prereqs'],
                            prerequisites=c['prerequisites'],
                            instructor=c['instructor'],
                            credit_hours=c['credit_hours'],
                            building=c['building'],
                            room=c['room'],
                            days=c['days'],
                            begin_time=c['begin_time'],
                            end_time=c['end_time'],
                            max_enroll=c['max_enroll'],
                            actual_enroll=c['actual_enroll'],
                            update_date=timezone.now())
        course.save()


def department_employee():
    with open('./QA/data/department_staff_json.json', 'r') as f:
        data = json.load(f)

    for d in data:
        department_id = d['department_id']
        department_info = d['department_info']['record']
        department_employees = d['department_employees']['records']

        department_email = None
        department_facebook = None
        department_website = None
        international_code = None
        area_code = None
        number = None
        extension = None

        if department_info['contacts']:
            if 'email' in department_info['contacts'].keys():
                department_email = department_info['contacts']['email'][0]

            if 'facebook' in department_info['contacts'].keys():
                department_facebook = department_info['contacts']['facebook'][0]

            if 'website' in department_info['contacts'].keys():
                department_website = department_info['contacts']['website'][0]

            if 'phone' in department_info['contacts'].keys():
                international_code = department_info['contacts']['phone'][0]['international_code']
                area_code = department_info['contacts']['phone'][0]['area_code']
                number = department_info['contacts']['phone'][0]['number']
                extension = department_info['contacts']['phone'][0]['extension']

        department = Department(
            department_id=department_id,
            parent_department_id=department_info['parent'],
            name=department_info['name'],
            descriptions=department_info['description'],
            contact_phone_international_code=international_code,
            contact_phone_area_code=area_code,
            contact_phone_number=number,
            contact_phone_extension=extension,
            contact_email=department_email,
            contact_facebook=department_facebook,
            contact_website=department_website,
            building=department_info['building'],
            update_date=timezone.now()

        )
        department.save()

        if department_employees:
            for e in department_employees:
                international_code = None
                area_code = None
                number = None
                extension = None
                title = None
                department = None
                if e['position']:
                    if e['position']['primary']:
                        if 'title' in e['position']['primary'].keys():
                            title = e['position']['primary']['title']
                        if 'department' in e['position']['primary'].keys():
                            department = e['position']['primary']['department']
                        if 'phone' in e['position']['primary'].keys():
                            international_code = e['position']['primary']['phone']['display']['international_code']
                            area_code = e['position']['primary']['phone']['display']['area_code']
                            number = e['position']['primary']['phone']['display']['number']
                            extension = e['position']['primary']['phone']['display']['extension']

                employee = Employee(
                    supervisor=e['supervisor'],
                    supervisee=e['supervises'],
                    tracks=e['tracks'],
                    first_name=e['name']['first'],
                    last_name=e['name']['last'],
                    middle_name=e['name']['middle'],
                    prefix_name=e['name']['prefix'],
                    suffix_name=e['name']['suffix'],
                    email=e['email'],
                    phone_international_code=international_code,
                    phone_area_code=area_code,
                    phone_number=number,
                    phone_extension=extension,
                    title=title,
                    position=e['position'],
                    department=department,
                    department_id=department_id,
                    update_date=timezone.now()

                )

                employee.save()


Department.objects.all().delete()
Employee.objects.all().delete()



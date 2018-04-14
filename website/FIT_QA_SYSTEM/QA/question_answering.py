from .models import *
import re
import spacy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .helpfunctions import *
import json
from .apiai_code import *
from string import Template

import apiai

#types: Building, Employee, Class
#answer type:
# location (map)
# person
# class
# message
# google url

nlp = spacy.load("./QA/data/FIT_model_b_c_e")


def translate(question_raw):
    #case sensitive: capitalize every word
    # words = question_raw.split()
    # words_c = [w.capitalize() for w in words]
    # question_translated = " ".join(words_c)
    question_translated = question_raw

    return question_translated


def answer_question(question):

    question = translate(question)
    doc = nlp(question)
    ents = doc.ents

    labels = [ent.label_ for ent in ents]


    if len(ents) == 1:
        if "FIT_BUILDING" in labels:
            # asking about buildings
            answer = answer_building(question, ents[0].text)
        elif "FIT_COURSE" in labels:
            # asking about course
            answer = answer_course(question, ents[0].text)
        elif "FIT_EMPLOYEE" in labels:
            answer = answer_employee(question, ents[0].text)
    elif small_talk(question)["answer_messages"][0]:
        answer = small_talk(question)
    else:
        answer = answer_url(question)

    return answer


def answer_building(question, keyword):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}

    building = Building.objects.filter(Q(building_code__iexact=keyword) | Q(building_name__iexact=keyword) | Q(building_abbr__iexact=keyword))
    if building:
        answer["answer_type"] = "string"

        if "name" in question.lower():
            for b in building:
                answer["answer_messages"].append(b.building_name)
        elif "code" in question.lower():
            for b in building:
                answer["answer_messages"].append(b.building_code)
        elif "address" in question.lower() or "location" in question.lower() or "where" in question.lower():
            answer["answer_type"] = "location"
            answer["length_range"] = range(len(building))
            for b in building:
                answer["answer_messages"].append((b.street+"\n"+b.city+", "+b.state+"\n"+b.zip+"\n", b.street))
        else:
            answer["answer_type"] = "building"
            answer["answer_obj"] = building

    else:
        answer["answer_type"] = "string"
        answer["answer_messages"].append("Sorry, it's not in our database. Please check your spelling.")
    return answer


def answer_course(question, keyword):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}

    course = Course.objects.filter(Q(crn__iexact=keyword) | Q(title__iexact=keyword) | Q(subject__iexact=keyword[:3], course_number__iexact=keyword[-4:]))

    if course:
        answer["answer_type"] = "string"
        if "instructor" in question.lower() or "teaches" in question.lower() or "teacher" in question.lower() or "who" in question.lower():
            for c in course:
                answer["answer_messages"].append("section " + c.section + "\n" + c.instructor)
        elif "location" in question.lower() or "classroom" in question.lower() or "where" in question.lower():
            answer["answer_type"] = "location"
            answer["length_range"] = range(len(course))
            for c in course:
                building = load_dirty_json(c.building)
                message = ("section " + c.section + "\n" + building["name"] + " " + c.room, building["street"])
                answer["answer_messages"].append(message)

        elif "time" in question.lower() or "when" in question.lower() or "days" in question.lower():
            for c in course:
                answer["answer_messages"].append("section " + c.section + "\n" + c.days + " " + c.begin_time + "-" + c.end_time)
        elif "prerequisite" in question.lower():
            for c in course:
                answer["answer_messages"].append("section " + c.section + "\n" + c.prerequisites)
        elif "capacity" in question.lower() or "enroll" in question.lower():
            for c in course:
                answer["answer_messages"].append("section " + c.section + "\n" + str(c.actual_enroll) + "/" + str(c.max_enroll))
        elif "credit" in question.lower():
            for c in course:
                answer["answer_messages"].append("section " + c.section + "\n" + str(c.credit_hours))
        else:
            answer["answer_type"] = "string"
            course_template = Template("CRN: $crn \nCode: $code \nSection: $section \n"
                                       "Title: $title \n Description: $description \n"
                                       "Instructor: $instructor \n"
                                       "Credit Hour: $credit_hour\n"
                                       "Location: $location\n"
                                       "Time: $time\n"
                                       "Actual Enrollment: $actual, Max Enrollment: $max")
            for c in course:
                building = load_dirty_json(c.building)
                course_str = course_template.substitute(crn=c.crn, code=c.subject+c.course_number, section=c.section,
                                           title=c.title, description=c.description, instructor=c.instructor,
                                           credit_hour=str(c.credit_hours), location=building["name"] + " " + c.room,
                                           time=c.days + " " + c.begin_time + "-" + c.end_time,
                                           actual=c.actual_enroll, max=c.max_enroll)
                answer["answer_messages"].append(course_str)


    else:
        answer["answer_type"] = "string"
        answer["answer_messages"].append("Sorry, it's not in our database. Please check your spelling.")

    return answer


def answer_employee(question, keyword):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}


    if "professor" in keyword.lower() or "prof" in keyword.lower() or "dr" in keyword.lower():
        keyword_list = keyword.split(" ")[1:]
        keyword = keyword_list.join(" ")

    if len(keyword.split(" ")) == 2:
        employee = Employee.objects.filter(Q(last_name__iexact=keyword) | Q(first_name__iexact=keyword) | Q(first_name__iexact=keyword.split(" ")[0], last_name__iexact=keyword.split(" ")[1]))
    else:
        employee = Employee.objects.filter(Q(last_name__iexact=keyword) | Q(first_name__iexact=keyword))

    if employee:
        answer["answer_type"] = "string"
        if "contact" in question.lower():
            for e in employee:
                answer["answer_messages"].append(e.first_name + " " + e.last_name + "\n" + 'email: ' + e.email + '\n phone: +' + e.phone_international_code + ' (' + e.phone_area_code + ') ' + e.phone_number)
        elif "email" in question.lower():
            for e in employee:
                answer["answer_messages"].append(e.first_name + " " + e.last_name + "\n" + e.email)
        elif "phone" in question.lower() or "number" in question.lower():
            for e in employee:
                answer["answer_messages"].append(e.first_name + " " + e.last_name + "\n" + e.phone_international_code + ' (' + e.phone_area_code + ') ' + e.phone_number)
        elif "where" in question.lower() or "office" in question.lower() or "find" in question.lower():
            answer["answer_type"] = "location"
            answer["length_range"] = range(len(employee))

            for e in employee:
                position = load_dirty_json(e.position.replace("None", "'None'"))

                primary = position["primary"]
                building = primary["building"]
                room = building["room"]
                message = (e.first_name + " " + e.last_name + "\n" + building["name"] + " " + room["number"], building["street"])
                answer["answer_messages"].append(message)


        else:
            answer["answer_type"] = "string"
            employee_template = Template("Name: $prefix $first_name $last_name \n"
                                       "Email: $email \n"
                                       "Phone: $phone \n"
                                       "Office: $office")
            for e in employee:
                position = load_dirty_json(e.position.replace("None", "'None'"))
                primary = position["primary"]
                building = primary["building"]
                room = building["room"]
                employee_str = employee_template.substitute(prefix=e.prefix_name, first_name=e.first_name, last_name=e.last_name,
                                                            email=e.email, phone=e.phone_international_code + ' (' + e.phone_area_code + ') ' + e.phone_number,
                                                            office=building["name"] + " " + room["number"])
                answer["answer_messages"].append(employee_str)
    else:
        answer["answer_type"] = "string"
        answer["answer_messages"].append("Sorry, it's not in our database. Please check your spelling.")
    return answer


def answer_frompassage(question):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}
    from googleapiclient.discovery import build
    service = build("customsearch", 'v1',developerKey="AIzaSyDjsBfa0igZZQUL6gMdDKEMIGsX6j-2HVA")
    res = service.cse().list(q=question, cx="006188269277128775091:loi0aooxt4w").execute()
    answer["answer_type"] = "url"
    answer["answer_messages"].append(res["url"])
    return answer

def answer_url(question):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}
    urlsearch = "https://www.google.com/search?q=site%3Afit.edu+" + question.replace(" ", "+").lower()
    answer["answer_type"] = "url"
    answer["answer_messages"].append(urlsearch)
    return answer


def small_talk(question):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}

    # Initialize API.AI client

    client = apiai.ApiAI(APIAI_CLIENT_ACCESS_TOKEN)

    # Create new request

    request = client.text_request()
    request.query = question

    # Receive response and convert it to JSON

    response = request.getresponse()


    answer["answer_type"] = "string"
    answer["answer_messages"].append(json.loads(response.read().decode())["result"]["fulfillment"]["speech"])

    return answer





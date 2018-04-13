from .models import *
import re
import spacy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .helpfunctions import *
import json

#types: Building, Employee, Class
#answer type:
# location (map)
# person
# class
# message
# google url

nlp = spacy.load("./QA/data/FIT_model_b_c_e")


def translate(question_raw):
    question_translated = question_raw
    return question_translated


def answer_question(question):
    print("answer_question from question answering")

    question = translate(question)
    doc = nlp(question)
    ents = doc.ents

    labels = [ent.label_ for ent in ents]

    answer = None


    if len(ents) == 1:
        if "FIT_BUILDING" in labels:
            # asking about buildings
            answer = answer_building(question, ents[0].text)
        elif "FIT_COURSE" in labels:
            # asking about course
            answer = answer_course(question, ents[0].text)
        elif "FIT_EMPLOYEE" in labels:
            answer = answer_employee(question, ents[0].text)
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
            answer["answer_type"] = "course"
            answer["answer_obj"] = course
    else:
        answer["answer_type"] = "string"
        answer["answer_messages"].append("Sorry, it's not in our database. Please check your spelling.")

    return answer


def answer_employee(question, keyword):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}

    print("employee")

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
                answer["answer_messages"].append(e.first_name + " " + e.last_name + "\n" + 'email: ' + e.email + ' phone: +' + e.phone_international_code + ' (' + e.phone_area_code + ') ' + e.phone_number)
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
            answer["answer_type"] = "employee"
            answer["answer_obj"] = employee
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






from .models import *
import re

def answer(question):
    cat = categorize_questions(question)

    if cat == "Location":
        result = answer_location(question)
        return result
    else:
        return {"answer": "this is the answer"}

def typeof(question):
    cat = categorize_questions(question)
    t=1
    if cat=="Location":
        t=2
    elif cat=="Instructor" or cat=="Class Time" or cat=="Classroom":
        t=0
    elif cat=="Office Hours" or cat=="Contact":
        t=0
    elif cat=="Building Hours":
        t=0
    return t


def preprocess(question):
    return question.lower()


def categorize_questions(question):
    preprocessed_question = preprocess(question)

    categories = ["Location", "Instructor", "Class Time", "Classroom", "Office Location", "Office Hours",
                  "Building Hours", "Contact", "Others"]

    if "location" in preprocessed_question or "where" in preprocessed_question or "address" in preprocessed_question:
        return "Location"
    else:
        return "Instructor"


def answer_location(question):
    where1 = re.compile(r"^[Ww]here is (?P<place>[ \w]+)(\?)?$")
    where2 = re.compile(r"^[Ww]hat is the location of (?P<place>[ \w]+)(\?)?$")
    where3 = re.compile(r"^[Ww]hat is the address of (?P<place>[ \w]+)(\?)?$")

    m1 = re.match(where1, question)
    m2 = re.match(where2, question)
    m3 = re.match(where3, question)

    if m1:
        place = m1.group('place')
    elif m2:
        place = m2.group('place')
    elif m3:
        place = m3.group('place')
    else:
        return {"answer": "Location not found"}

    building_code_pattern = re.compile(r"[\d]{3,3}[\w]{3,3}")

    if re.match(building_code_pattern, place):
        b = Building.objects.get(building_code=place)
    else:
        b = Building.objects.get(building_name=place)

    return {"answer": b.street, "lat": b.latitude, "long":b.longitude}





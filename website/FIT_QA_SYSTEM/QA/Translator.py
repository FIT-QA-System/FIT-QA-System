from .models import *
import pickle
import re
import spacy
import json
import django


def hasevent(question):
    if "event" in question:
        return True
    return False


def hasdate(question):
    if "date" in question:
        return True
    return False


def has_class(question):

    #nlp = spacy.load("en_core_web_sm")


    course_re1= re.compile(r"^[\w ]+ (?P<course_subject>[\w]{3,3})(?P<course_code>[\d]{4,4})[\w ]*(\?)?$")
    course_re2 = re.compile(r"^[\w ]+ (?P<course_title>[\w])[\w ]*(\?)?$")
    course_match1 = re.match(course_re1, question)
    course_match2 = re.match(course_re2, question)
    if course_match1:
        c_subject = course_match1.group("course_subject")
        c_code = course_match1.group("course_code")
        answer_course = Course.objects.filter(subject=c_subject, course_number=c_code)
        if answer_course:
            return True

    elif course_match2:
        c_title = course_match2.group("course_title")
        answer_course = Course.objects.filter(title=c_title)
        if answer_course:
            return True
    return False

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
    elif cat=="Class":
        t=0
    return t


def hasfaculty(question):
    words=question.split(' ')
    del words[0]
    for word in words:
        if word[0].isupper():
            if "Dr."in word:
                name=word[3:]
                if Employee.objects.filter(first_name=name) or Employee.objects.filter(last_name=name):
                    return True
            else:
                name = word
                if Employee.objects.filter(first_name=name) or Employee.objects.filter(last_name=name):
                    return True
    return False

def hasbuilding(question):
    #with open('data/buildings.json', 'r') as f:
      #  data = json.load(f)

    #buildings = data['records']
    #nlp = spacy.load("en")

    #building = nlp(question).ents[0].text
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
        return False

    building_code_pattern = re.compile(r"[\d]{3,3}[\w]{3,3}")

    if re.match(building_code_pattern, place):
        b = Building.objects.get(building_code=place)
    else:
        b = Building.objects.get(building_name=place)

    if b:
        return True
    return False


def categorize_questions(question):
    
    categories=["Location","Instructor","Class Time","Classroom","Office Location","Office Hours","Building Hours","Contact","Others"]
    #maxsimilarity = 0
    #tags = pos_tag(word_tokenize(question))
    #print(nltk.ne_chunk(tags))
    ##building hours:
    if "When" in question or "when" in question or "time" in question: #1.1 & 1.3 & 1.4 & 1.5, 1.2
        if hasbuilding(question):
            return categories[6]
    if "open" in question or "close" in question or "closed" in question:
        if "Why" in question or "How" in question:
            return categories[8]
        return categories[6]
    if "building hours" in question:
        return categories[6]
    ##instructor
    if "instructor" in question or "teacher" in question or "teaches" in question: #2.1 2.2 2.3 class info-instructor=who+class title
   #     for word in tags:
   #         if pos_tag(word)[1]==
        if has_class(question):
            return categories[1]
    ##class time
    if "what" in question or "What" in question:
        if "time" in question:
            if has_class(question):
                return categories[2] ##3.1
    if "when" in question or "When" in question:
        if has_class(question):
            return categories[2] ##3.2 3.3
    ##classroom location
    if "Where" in question or "where" in question or "location" in question or "Which building" in question:
        if has_class(question):
            return categories[3] ##4.1 4.2 4.3
    ##faculty office location
    if "Where" in question or "where" in question or "location" in question:
        if hasbuilding(question):
            return categories[0]
        if hasfaculty(question):
            if "from" in question:
                return categories[8]
            return categories[4] ##5.1 5.2
        
    ##office hours
    if "office hours" in question or "When" in question and "office" in question:
        return categories[5]##6.2
    ##contact
    if "contact" in question or "email" in question or "phone number" in question:
        if hasfaculty(question):
            return categories[7] ##7.1 7.2
    if "When" in question:
        if hasevent(question):
            return "Calendar"
    if "event" in question:
        if hasdate(question):
            return "Calendar"
    
    #for sample in samples:
    #    similarity = sentence_similarity(question,sample)
    #    if similarity > maxsimilarity:
    #        maxsimilarity = similarity
    #        category = sample
    return categories[8]


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
        return "Location not found"

    building_code_pattern = re.compile(r"[\d]{3,3}[\w]{3,3}")

    if re.match(building_code_pattern, place):
        b = Building.objects.get(building_code=place)
    else:
        b = Building.objects.get(building_name=place)

    return b.street


def answer_class(question,subtype):
    first_word = question.split(" ")[0].lower()

    nlp = spacy.load("en_core_web_sm")

    result = {}

    course_re = re.compile(r"^[\w ]+ (?P<course_subject>[\w]{3,3})(?P<course_code>[\d]{4,4})[\w ]*(\?)?$")

    course_match = re.match(course_re, question)

    if course_match:
        c_subject = course_match.group("course_subject")
        c_code = course_match.group("course_code")

        answer_course = Course.objects.filter(subject=c_subject, course_number=c_code)

    else:
        entities = nlp(question).ents
        if len(entities) == 0:
            answer_course = None
        else:
            course = entities[0].text
            answer_course = Course.objects.filter(title=course)

    if answer_course:
        answer_course = answer_course[0]
        if first_word == "who":
            result = answer_course.instructor
        elif first_word == "where":
            result = answer_course.building + " " + answer_course.room
        elif first_word == "when":
            result = answer_course.days + " " + answer_course.begin_time + "-" + answer_course.end_time
        elif first_word == "what":
            if question.split(" ")[1].lower() == "time":
                result = answer_course.begin_time + "-" + answer_course.end_time
            elif question.split(" ")[1].lower() == "days":
                result = answer_course.days
        elif "enrollment" in question or "enroll" in question or "capacity" in question:
            result = "capacity: " + str(answer_course.max_enroll) + ", " + "actual enroll: " + str(
                answer_course.actual_enroll)
        else:
            result = str(answer_course)

    else:
        result = "Class not found"

    return result


def answer_staff(question,cat):
    words = question.split(' ')
    del words[0]
    staff=None
    for word in words:
        if word[0].isupper():
            if "Dr." in word:
                name = word[3:]
                if Employee.objects.filter(first_name=name):
                    staff=Employee.objects.filter(first_name=name)[0]
                elif Employee.objects.filter(last_name=name):
                    staff = Employee.objects.filter(last_name=name)[0]
            else:
                name = word
                if Employee.objects.filter(first_name=name):
                    staff=Employee.objects.filter(first_name=name)[0]
                elif Employee.objects.filter(last_name=name):
                    staff = Employee.objects.filter(last_name=name)[0]
    astaff=None
    if staff:
        if cat=="Contact":
            astaff='email: '+staff.email+' phone: +'+staff.phone_international_code+' ('+staff.phone_area_code+') '+staff.phone_number
        else:
            astaff=staff.title+' '+staff.first_name+' '+staff.last_name+' '+staff.email+' '+staff.department
    return astaff


def answer_buildinghours(question):
    return "hours"


def answer_frompassage(question):
    from googleapiclient.discovery import build
    service = build("customsearch", 'v1',developerKey="AIzaSyDjsBfa0igZZQUL6gMdDKEMIGsX6j-2HVA")
    res = service.cse().list(q=question, cx="006188269277128775091:loi0aooxt4w").execute()
    return res['url']


def exists(question):
    return False;


def get_answer(question):
    return "old"


def answer(question):
    if exists(question):
        answer=get_answer(question)
        return answer
    cat = categorize_questions(question)
    if cat == "Location":
        answer = answer_location(question)
    elif cat=="Instructor" or cat=="Class Time" or cat=="Classroom":
        answer = answer_class(question,cat)
    elif cat=="Office Location" or cat=="Office Hours" or cat=="Contact":
        answer = answer_staff(question,cat)
    elif cat=="Building Hours":
        answer = answer_buildinghours(question)
    else:
        answer = answer_frompassage(question)
    return answer


import pickle
import re
import spacy
import json
from Milestone2.course_info.get_info import Course

def hasclass(question):
    courses = pickle.load(open("Milestone2/course_info/courses.txt", "rb"))
    #nlp = spacy.load("en")

   # print(nlp(question))
    #course = nlp(question).ents[0].text

    answer_course = None

    for c in courses:
        if c.title in question:
            answer_course = c
    if answer_course!=None :
        return True
    return False


def hasfaculty(question):
    with open('data/department_staff_json.json', 'r') as f:
        data = json.load(f)
    for d in data:
        astaff=None
        staff = d['department_employees']['records']
        if staff!=None:
            for s in staff:
                if s['name']['first'] in question or s['name']['last'] in question:
                    astaff = s
        if astaff!=None :
            return True
    #nlp = spacy.load("en")

    #building = nlp(question).ents[0].text

    return False

def hasbuilding(question):
    with open('data/buildings.json', 'r') as f:
        data = json.load(f)

    buildings = data['records']
    nlp = spacy.load("en")

    #building = nlp(question).ents[0].text
    answer_building = None

    for b in buildings:
        if b['code'] in question or b['name'] in question:
            answer_building = b
    if answer_building!=None :
        return True
    return False
def hasevent(question):
    if "event" in question:
        return True
    return False
def hasdate(question):
    if "date" in question:
        return True
    return False
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import treebank as tb
from nltk.corpus.reader.wordnet import WordNetError
from nltk import word_tokenize, pos_tag 

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
        if hasclass(question):
            return categories[1]
    ##class time
    if "what" in question or "What" in question:
        if "time" in question:
            if hassclass(question):
                return categories[2] ##3.1
    if "when" in question or "When" in question:
        if hasclass(question):
            return categories[2] ##3.2 3.3
    ##classroom location
    if "Where" in question or "where" in question or "location" in question or "Which building" in question:
        if hasclass(question):
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
    with open('data/buildings.json', 'r') as f:
        data = json.load(f)
    nlp = spacy.load("en")
    buildings = data['records']
    #print(nlp(question))
    #building = nlp(question).ents[0].text

    ab = None

    for b in buildings:  ##index(hashtable(unique key--ID,multiple indices,can be course number,building number,teacher,+value, can ask database to do it), tree) on top of data
        if b['code'] in question or b['name'] in question:
            ab = b
    return ab['street']+' '+str(ab['number'])
def answer_class(question,subtype):
    courses = pickle.load(open("Milestone2/course_info/courses.txt", "rb"))
    #nlp = spacy.load("en")

    #print(nlp(question))
    #course = nlp(question).ents[0].text

    answer_course = None

    for c in courses:  ##index(hashtable(unique key--ID,multiple indices,can be course number,building number,teacher,+value, can ask database to do it), tree) on top of data
        if c.title in question:
            answer_course = c
    #print(answer_course)
    if subtype == "Instructor":
        return answer_course.instructor
    elif subtype == "Classroom":
        return answer_course.place
    elif subtype == "Class Time":
        return answer_course.days + " " + answer_course.time
    else:
        return answer_course.__dict__
def answer_staff(question,cat):
    with open('data/department_staff_json.json', 'r') as f:
        data = json.load(f)
    astaff=None
    for d in data:
        
        staff = d['department_employees']['records']
        if staff!=None:
            for s in staff:
                if s['name']['first'] in question or s['name']['last'] in question:
                    if cat=="Office Location":
                        if 'building' in s['position']['primary'].keys():
                            astaff=s['position']['primary']['building']['code']+' '+str(s['position']['primary']['building']['number'])
                    elif cat=="Contact":
                        astaff='email: '+s['email']
                        if 'phone' in s['position']['primary'].keys():
                            astaff = astaff+' '+'phone: '+s['position']['primary']['phone']['display']["area_code"]+s['position']['primary']['phone']['display']["number"]

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
    if cat=="Location":
        answer = answer_location(question)
    elif cat=="Instructor" or cat=="Class Time" or cat=="Classroom":
        answer = answer_class(question,cat);
    elif cat=="Office Location" or cat=="Office Hours" or cat=="Contact":
        answer = answer_staff(question,cat);
    elif cat=="Building Hours":
        answer = answer_buildinghours(question);
    else:
        answer = answer_frompassage(question);
    return answer

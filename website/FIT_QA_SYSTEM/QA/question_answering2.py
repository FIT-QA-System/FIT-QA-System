from .models import *
import re
import spacy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .helpfunctions import *
import json
from .apiai_code import *
from string import Template
from .answernews import *

import apiai

#types: Building, Employee, Class
#answer type:
# location (map)
# person
# class
# message
# google url

nlp = spacy.load("./QA/data/FIT_model_b_c_e")

fit_ner = None
with open("./QA/data/FIT_dictionary.txt", "r") as f:
    lines = f.readlines()
    words = set(lines)
    fit_ner = [w.replace("\n","") for w in words]

def translate(question_raw):
    standard_pairs = Word_Standard.objects.all()

    for s in standard_pairs:
        if s.original_word.lower() in question_raw.lower() and s.standard_word.lower() not in question_raw.lower():
            question_raw = question_raw.replace(s.original_word, s.standard_word)
            question_raw = question_raw.replace(s.original_word.lower(), s.standard_word)
            break

    doc_raw = nlp(question_raw)
    #case sensitive: capitalize every word
    question_capitalized = question_raw.title()

    doc_capitalized = nlp(question_capitalized)

    if doc_capitalized.ents == doc_raw.ents:
        return question_raw

    ents = doc_capitalized.ents

    question_translated = question_raw

    for ent in ents:
        if ent.text in fit_ner:
            raw_text = "".join([t.lower() for t in ent.text])
            question_translated = question_raw.replace(raw_text, ent.text)

    return question_translated

import pickle
#import spacy
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError
from nltk import word_tokenize, pos_tag   ##implementation of similarity() from http://nlpforhackers.io/wordnet-sentence-similarity/
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
def pathsim(ss1, ss2):
    if ss1.path_similarity(ss2) is None:
        return 0
    return ss1.path_similarity(ss2)
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    NoneType = type(None)
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence1nv = []
    sentence2 = pos_tag(word_tokenize(sentence2))
    sentence2nv = []
    # Get the synsets for the tagged words
    synsets1 = []
    count1 = 0
    count2=0
    tup = ()
    synsetnone1 = []
    for tagged_word in sentence1:
        if type(tagged_to_synset(*tagged_word))== NoneType and tagged_word[0][0].isupper() and penn_to_wn(tagged_word[1]) == 'n':
            count1 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence1nv.append(tup)
            synsetnone1.append(tup)
            continue
        if penn_to_wn(tagged_word[1]) == 'n':
            count1 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence1nv.append(tup)
    synsets2 = []
    tup = ()
    synsetnone2 = []
    for tagged_word in sentence2:
        if type(tagged_to_synset(*tagged_word))== NoneType and tagged_word[0][0].isupper() and penn_to_wn(tagged_word[1]) == 'n':
            count2+=1
            tup = (tagged_word[0], tagged_word[1])
            sentence2nv.append(tup)
            synsetnone2.append(tup)
            continue
        if penn_to_wn(tagged_word[1]) == 'n':
            count2+=1
            tup = (tagged_word[0], tagged_word[1])
            sentence2nv.append(tup)
    synsets1 = [tagged_to_synset(tagged_word, tag) for tagged_word, tag in sentence1nv]
    synsets2 = [tagged_to_synset(tagged_word, tag) for tagged_word, tag in sentence2nv]
    
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if not type(ss) == NoneType]
    synsets2 = [ss for ss in synsets2 if not type(ss) == NoneType]
    score = 0.0
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        if not synsets2 == []:
            best_score = max([pathsim(synset, ss) for ss in synsets2])
        # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
    for synset in synsets2:
        # Get the similarity value of the most similar word in the other sentence
        if not synsets1 == []:
            best_score = max([pathsim(synset, ss) for ss in synsets1])
        # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
    for synsetnone in synsetnone2:
        if synsetnone in synsetnone1:
            score += 1
    for synsetnone in synsetnone1:
        if synsetnone in synsetnone2:
            score += 1
    # Average the values
    score /= (count1 + count2)
    return score
def match(words,line):
    hit=0
    qs=line.split()
    n=len(words)
    for word in words:
        if word==None:
            n=n-1
            continue
        if word in line:
            hit=hit+1
    return hit/n

def answer_question(question):

    question = translate(question)
    doc = nlp(question)
    ents = doc.ents

    labels = [ent.label_ for ent in ents]

    print(ents)

    if len(ents) == 1:
        if "FIT_BUILDING" in labels:
            # asking about buildings
            print("building")
            answer = answer_building(question, ents[0].text)
        elif "FIT_COURSE" in labels:
            # asking about course
            print("course")
            answer = answer_course(question, ents[0].text)
        elif "FIT_EMPLOYEE" in labels:
            print("employee")
            answer = answer_employee(question, ents[0].text)
    elif small_talk(question)["answer_messages"][0]:
        print("small_talk")
        answer = small_talk(question)
    else:
        answer = answernews(question)
        if answer==None:
            print("url")
            answer = answer_url(question)

    return answer

def answernews(question):
#nlp = spacy.load("en")
#who, when, where
    if "who" in question or "Who" in question: #named entity checking
        words=question.split()
        qs=pos_tag(word_tokenize(question))
        for i in range(len(words)):
            if penn_to_wn(qs[i][1]) != 'n':
                words[i]=None
            elif words[i][0].isupper:
                words.append(words[i])
        for index, line in enumerate(open('data/news.txt', 'r').readlines()):
            if match(words,line)>0.75:
                #print(match(words,line))
                #print(ne_chunk(pos_tag(word_tokenize(line))))
                for subtree in ne_chunk(pos_tag(word_tokenize(line))).subtrees():
                    if subtree.label()=="PERSON":
                        return subtree.leaves()[0][0]+' '+subtree.leaves()[1][0]
                return line
    if "when" in question or"When" in question:
        words=question.split()
        qs=pos_tag(word_tokenize(question))
        for i in range(len(words)):
            if penn_to_wn(qs[i][1]) != 'n':
                words[i]=None
            elif words[i][0].isupper:
                words.append(words[i])
        for index, line in enumerate(open('data/news.txt', 'r').readlines()):
            if match(words,line)>0.70:
                #print(match(words,line))
                #print(ne_chunk(pos_tag(word_tokenize(line))))
                for subtree in ne_chunk(pos_tag(word_tokenize(line))).subtrees():
                    if subtree.label()=="CD":
                        return subtree.leaves()
                return line
    if "where"in question or"Where" in question:
        words=question.split()
        qs=pos_tag(word_tokenize(question))
        for i in range(len(words)):
            if penn_to_wn(qs[i][1]) != 'n':
                words[i]=None
            elif words[i][0].isupper:
                words.append(words[i])
        for index, line in enumerate(open('data/news.txt', 'r').readlines()):
            if match(words,line)>0.70:
                #print(match(words,line))
                #print(ne_chunk(pos_tag(word_tokenize(line))))
                for subtree in ne_chunk(pos_tag(word_tokenize(line))).subtrees():
                    if subtree.label()=="GPE":
                        return subtree.leaves()
                return line
    else:
        for index, line in enumerate(open('data/news.txt', 'r').readlines()):
            if sentence_similarity(line,question)>0.70:
                return line
    return None
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
            answer["answer_type"] = "location"
            building_template = Template("Name: $name\n"
                                         "Code: $code\n"
                                         "Address: $address\n")
            for b in building:
                building_str = building_template.substitute(name=b.building_name, code=b.building_code, address=b.street+"\n"+b.city+", "+b.state+"\n"+b.zip+"\n")
                answer["answer_messages"].append((building_str, b.street))


    else:
        answer["answer_type"] = "string"
        answer["answer_messages"].append("Sorry, it's not in our database. Please check your spelling.")
    return answer


def answer_course(question, keyword):
    answer = {"answer_type": None, "answer_messages": [], "answer_locations": [], "answer_obj": None}

    course = Course.objects.filter(Q(crn__iexact=keyword) | Q(title__iexact=keyword) | Q(subject__iexact=keyword[:3], course_number__iexact=keyword[-4:]) | Q(subject__iexact=keyword))

    if course:
        answer["answer_type"] = "string"
        if "instructor" in question.lower() or "teaches" in question.lower() or "teacher" in question.lower() or "who" in question.lower():
            for c in course:
                answer["answer_messages"].append("section " + c.section + "\n" + c.instructor)
        elif "location" in question.lower() or "classroom" in question.lower() or "class room" in question.lower() or "where" in question.lower():
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
                location_str = "TBA"
                if c.building != "TBA":
                    building = load_dirty_json(c.building.replace("None", "'None'"))
                    location_str = building["name"] + " " + c.room

                course_str = course_template.substitute(crn=c.crn, code=c.subject+c.course_number, section=c.section,
                                           title=c.title, description=c.description, instructor=c.instructor,
                                           credit_hour=str(c.credit_hours), location=location_str,
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





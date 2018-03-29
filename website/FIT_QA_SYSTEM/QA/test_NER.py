import spacy
from string import Template
from .models import *
import random
import os
import pickle

nlp = spacy.load("en_core_web_sm")



questions = ["What does Dr. Chan teach?",
             "Where is Panther Dining Hall?",
             "The instructor of CSE4001 is Ribero?",
             "What is the email address of the Computer Science Department?",
             "Tell me about ABA Technologies, Inc."]

#Building Template
location_template = []
location_template.append("Where is $building?")
location_template.append("What is the address of $building?")
location_template.append("What is the location of $building?")
location_template.append("How can I get to $building?")
location_template.append("Where is $building located?")

#Course_Template
#course: 1. course name 2. crn (all digits), 3. course code (CSE4102)
course_template = []
course_template.append("Who is the instructor of $course?")
course_template.append("Who teaches $course?")
course_template.append("When is $course?")
course_template.append("Which classroom is $course in?")
course_template.append("Where is $course?")
course_template.append("What days are $course?")
course_template.append("What is the capacity of $course?")
course_template.append("How many people are enrolled in $course?")
course_template.append("What is the crn of $course?")
course_template.append("When does $course start?")
course_template.append("How many credit hours are $course?")
course_template.append("What is the prerequisite of $course?")
course_template.append("Show me all sections of $course.")

#"What classes does x teach?"


def get_entity(sentence, ne, label_name):

    start_index = sentence.index(ne)
    end_index = start_index + len(ne)

    return (sentence, {'entities':[(start_index, end_index, label_name)]})


def get_entity2(sentence, ne, label_name):

    start_index = sentence.index(ne)
    end_index = start_index + len(ne)

    return (sentence, [(start_index, end_index, label_name)])

def generate_example(obj, templates, substitute_str, label_name):
    template_str = random.choice(templates)
    template = Template(template_str)
    sentence = None
    if(substitute_str == "$building"):
        sentence = template.substitute(building=obj)
    elif(substitute_str == "$course"):
        sentence = template.substitute(course=obj)

    return get_entity2(sentence, obj, label_name)

def generate_training():
    training_set = []

    buildings = Building.objects.all()
    courses = Course.objects.all()

    for b in buildings:
        training_set.append(generate_example(b.building_name, location_template, "$building", "FIT_BUILDING"))
        training_set.append(generate_example(b.building_code, location_template, "$building", "FIT_BUILDING"))
    for c in courses:
        training_set.append(generate_example(c.crn, course_template, "$course", "FIT_COURSE"))
        training_set.append(generate_example(c.title, course_template, "$course", "FIT_COURSE"))
        training_set.append(generate_example(c.subject + c.course_number, course_template, "$course", "FIT_COURSE"))

    with open("./QA/data/news_sentences.txt", "r") as f:
        sentences = f.readlines()
        for s in sentences:
            ents = [(e.start_char, e.end_char, e.label_) for e in nlp(s).ents]
            training_set.append((s, {'entities': ents}))

    pickle.dump(training_set, open("./QA/data/training_sentences.txt", "wb"))

    return training_set

def generate_training2():
    training_set = []

    buildings = Building.objects.all()
    courses = Course.objects.all()

    for b in buildings:
        training_set.append(generate_example(b.building_name, location_template, "$building", "FIT_BUILDING"))
        training_set.append(generate_example(b.building_code, location_template, "$building", "FIT_BUILDING"))
    for c in courses:
        training_set.append(generate_example(c.crn, course_template, "$course", "FIT_COURSE"))
        training_set.append(generate_example(c.title, course_template, "$course", "FIT_COURSE"))
        training_set.append(generate_example(c.subject + c.course_number, course_template, "$course", "FIT_COURSE"))

    with open("./QA/data/news_sentences.txt", "r") as f:
        sentences = f.readlines()
        for s in sentences:
            ents = [(e.start_char, e.end_char, e.label_) for e in nlp(s).ents]
            training_set.append((s, ents))

    pickle.dump(training_set, open("./QA/data/training_sentences2.txt", "wb"))

    return training_set



if __name__ == "__main__":
    print(generate_training()[:10])
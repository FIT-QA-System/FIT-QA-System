import spacy
from string import Template
from .models import *
import random

nlp = spacy.load("en_core_web_sm")



questions = ["What does Dr. Chan teach?",
             "Where is Panther Dining Hall?",
             "The instructor of CSE4001 is Ribero?",
             "What is the email address of the Computer Science Department?",
             "Tell me about ABA Technologies, Inc."]

#Building Template
location_template = []
location_template[0] = "Where is $building?"
location_template[1] = "What is the address of $building?"
location_template[2] = "What is the location of $building?"
location_template[3] = "How can I get to $building?"
location_template[4] = "Where is $building located?"

#Course_Template
#course: 1. course name 2. crn (all digits), 3. course code (CSE4102)
course_template = []
course_template[0] = "Who is the instructor of $course?"
course_template[1] = "Who teaches $course?"
course_template[2] = "When is $course?"
course_template[3] = "Which classroom is $course in?"
course_template[4] = "Where is $course?"
course_template[5] = "What days are $course?"
course_template[6] = "What is the capacity of $course?"
course_template[7] = "How many people are enrolled in $course?"
course_template[8] = "What is the crn of $course?"
course_template[9] = "When does %course start?"
course_template[10] = "How many credit hours are $course?"
course_template[11] = "What is the prerequisite of $course?"
course_template[12] = "Show me all sections of $course."

#"What classes does x teach?"


def get_entity(sentence, ne, label_name):

    start_index = sentence.index(ne)
    end_index = start_index + len(ne)

    return (sentence, {'entities':[(start_index, end_index, label_name )]})



def generate_training():
    training_set = []

    buildings = Building.objects.all()
    courses = Course.objects.all()

    for b in buildings:
        template = random.choice(location_template)





    return training_set


if __name__ == "__main__":
    for q in questions:
        ents = [(e.text, e.start_char, e.end_char, e.label_) for e in nlp(q).ents]
        print(ents)
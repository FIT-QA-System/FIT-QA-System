import pickle
import re
import spacy
from get_info import Course


courses = pickle.load(open("courses.txt", "rb"))

test_questions = ["Where is Intro to Human Factors?",
                  "Who is the instructor of Intro to Human Factors?",
                  "When is Intro to Human Factors?",
                  "What time does Intro to Human Factors start?",
                  "What days do we have Intro to Human Factors?",
                  "Give me all information about Intro to Human Factors."]

test_questions_2 = "Where is the classroom for Content Area Reading?"


# TODO check class title format, some classes are not found

# TODO group questions by what field should be returned

# TODO re


def entities(questions):
    nlp = spacy.load("en")

    for q in questions:
        doc = nlp(q)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            print()




def answer_question(question):
    first_word = question.split(" ")[0].lower()

    nlp = spacy.load("en")

    print(nlp(question).ents)
    course = nlp(question).ents[0].text

    answer_course = None

    for c in courses:
        if c.title == course:
            answer_course = c

    if first_word == "who":
        print(answer_course.instructor)
    elif first_word == "where":
        print(answer_course.place)
    elif first_word == "when":
        print(answer_course.days + " " + answer_course.time)
    elif first_word == "what":
        if question.split(" ")[1].lower() == "time":
            print(answer_course.time)
        elif question.split(" ")[1].lower() == "days":
            print(answer_course.days)
    else:
        print(answer_course.__dict__)





if __name__ == "__main__":
    # entities(test_questions)
    for q in test_questions:
        answer_question(q)
    print("test======")
    answer_question(test_questions_2)




import spacy
from string import Template

nlp = spacy.load("en_core_web_sm")



questions = ["What does Dr. Chan teach?",
             "Where is Panther Dining Hall?",
             "The instructor of CSE4001 is Ribero?",
             "What is the email address of the Computer Science Department?",
             "Tell me about ABA Technologies, Inc."]

#Building Template
location_template = []
location_template[0] = Template("Where is $building?")
location_template[1] = Template("What is the address of $building?")
location_template[2] = Template("What is the location of $building?")
location_template[3] = Template("How can I get to $building?")
location_template[4] = Template("Where is $building located?")

#Course_Template
#course: 1. course name 2. crn (all digits), 3. course code (CSE4102)
course_template = []
course_template[0] = Template("Who is the instructor of $course?")
course_template[1] = Template("Who teaches $course?")
course_template[2] = Template("When is $course?")
course_template[3] = Template("Which classroom is $course in?")
course_template[4] = Template("Where is $course?")
course_template[5] = Template("What days are $course?")
course_template[6] = Template("What is the capacity of $course?")
course_template[7] = Template("How many people are enrolled in $course?")
course_template[8] = Template("What is the crn of $course?")
course_template[9] = Template("When does %course start?")
course_template[10] = Template("How many credit hours are $course?")
course_template[11] = Template("What is the prerequisite of $course?")
course_template[12] = Template("Show me all sections of $course.")

#"What classes does x teach?"



def generate_training():
    training_set = []

    return training_set


if __name__ == "__main__":
    for q in questions:
        ents = [(e.text, e.start_char, e.end_char, e.label_) for e in nlp(q).ents]
        print(ents)
from models import Course

import pickle


courses = pickle.load(open("courses.txt", "rb"))

for c in courses:
    course = Course(CRN=c.CRN, subject=c.subject, section=c.section, credit=c.credit, title=c.title, description=c.description, notes=c.notes, days=c.days, time=c.time, place=c.place, instructor=c.instructor, enrolled=c.enrolled, limit=c.limit, semester=c.semester)
    course.save()
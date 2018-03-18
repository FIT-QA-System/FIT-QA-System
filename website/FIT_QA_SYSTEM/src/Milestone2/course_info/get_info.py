from bs4 import BeautifulSoup
import pickle


class Course(object):
    CRN = ""
    department = ""
    number = ""
    subject = ""
    section = ""
    credit = ""
    title = ""
    description = ""
    notes = ""
    days = ""
    time = ""
    place = ""
    instructor = ""
    enrolled = 0
    limit = 0
    semester = ""
    year = ""

    def __init__(self, CRN, subject, section, credit, title, description, notes, days, time, place, instructor, enrolled, limit, semester):
        self.CRN = CRN
        self.subject = subject
        self.section = section
        self.credit = credit
        self.title = title
        self.description = description
        self.notes = notes
        self.days = days
        self.time = time
        self.place = place
        self.instructor = instructor
        self.enrolled = enrolled
        self.limit = limit
        self.semester = semester


    def answer(self, type):
        if type == "location":
            return self.place
        if type == "datetime":
            return self.days + " " + self.time
        if type == "credit":
            return self.credit
        if type == "CRN":
            return self.CRN
        if type == "title":
            return self.title
        if type == "subject":
            return self.subject
        if type == "instructor":
            return self.instructor
        if type == "enrolled":
            return self.enrolled
        if type == "limit":
            return self.enrolled
        if type == "enrollment":
            return str(self.enrolled) + "/" + str(self.limit)



def get_course_info(html, semester):
    courses = []
    bs = BeautifulSoup(html, "lxml")

    trs = bs.find_all("tr")

    for tr in trs:
        tds = tr.find_all("td")

        CRN = tds[0].get_text()
        subject = tds[1].get_text()
        section = tds[2].get_text()
        credit = tds[3].get_text()
        title = tds[4].find_all("span")[0].get_text()
        description = tds[4].find_all("span")[0]["data-original-title"]
        notes = tds[5].get_text()
        days = tds[6].get_text().replace("\n", "")
        time = tds[7].get_text().replace("\n", "")
        place = tds[8].get_text().replace("\n", "")
        instructor = tds[9].get_text()
        enrolled = int(tds[10].get_text().split("/")[0])
        limit = int(tds[10].get_text().split("/")[1])

        course = Course(CRN, subject, section, credit, title, description, notes, days, time, place, instructor, enrolled, limit, semester)

        courses.append(course)

    return courses


if __name__ == "__main__":
    # html = open("./spring2018.html").read()
    #
    # courses = get_course_info(html, "spring 2018")
    #
    # pickle.dump(courses, open("courses.txt", "wb"))

    courses = pickle.load(open("courses.txt", "rb"))

    print(courses[0].__dict__)

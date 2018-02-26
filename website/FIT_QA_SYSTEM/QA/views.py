from django.http import HttpResponse
import re

from .models import *

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def question_detail(request, question):
    return HttpResponse("The answer is %s." % answer_building_question(question=question))

def answer_building_question(question):
    question = question.replace("%20", " ").lower()
    where = re.compile(r"^where is (?P<place>\w+)(\?)?$")

    m = re.match(where, question)
    print(m.group('place'))

    result = m.group('place').upper()

    b = Building.objects.get(building_code=result)

    return b.building_name + " " + b.street + " " + b.city + "\n"

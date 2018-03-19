from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import re
from .models import *
from .forms import QuestionForm
# from src.Translator import answer, typeof


def index(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['question']
            a = answer(q)
            t = typeof(q)
            if typeof(q) == 2:
                a = a.replace(" ","+").lower()

            return render(request, 'answer.html', {'question': q, 'answer': a, 'type': t})

    return render(request, 'index.html')

def answer(question):
    return "this is answer"

def typeof(question):
    return 2

def question_detail(request, question):
    return render(request, 'answer.html', answer=answer_building_question(question=question))

def answer_building_question(question):
    question = question.replace("%20", " ").lower()
    where = re.compile(r"^where is (?P<place>\w+)(\?)?$")

    m = re.match(where, question)
    print(m.group('place'))

    result = m.group('place').upper()

    b = Building.objects.get(building_code=result)

    return b.building_name + " " + b.street + " " + b.city + "\n"

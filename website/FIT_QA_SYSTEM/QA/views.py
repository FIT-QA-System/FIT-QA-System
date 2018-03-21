from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import re
from .models import *
from .forms import QuestionForm
#from .question_answering import *
from .Translator import *


def index(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['question']
            result = answer(q)
            a = None
            t = typeof(q)
            b_street = None

            if typeof(q) == 2:
                if result['answer'] == "Location not found":
                    t = 0
                else:
                    a = result['answer']
                    b_street = result['answer'].replace(" ", "+").lower()
            elif typeof(q) == 1:
                a = "Can't answer the question"
                t=0
            else:
                a = result['answer']

            return render(request, 'answer.html', {'question': q, 'answer': a, 'type': t, 'building_street': b_street})

    return render(request, 'index.html')


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

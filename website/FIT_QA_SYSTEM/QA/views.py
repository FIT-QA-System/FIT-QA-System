from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import re
from .models import *
from .forms import QuestionForm
#from .question_answering import *
from .Translator import *
from .test_NER import *
import pickle
import json
from django.core.exceptions import *

def index(request):
    pq = []
    for paqu in PastQuestion.objects.all():
        pq.append(paqu.question)
    pq=json.dumps(pq)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['question']
            result = answer(q)
            a = result
            t = typeof(q)
            b_street = None
            urlsearch = None

            if typeof(q) == 2:
                if a == "Location not found":
                    t = 0
                else:
                    b_street = a.replace(" ", "+").lower()
            elif typeof(q) == 1:
                urlsearch = "https://www.google.com/search?q=" + q.replace(" ", "+").lower()
                a = "I can't answer that question "
            else:
                a = result

            try:
                PastQuestion.objects.get(question=q)
            except ObjectDoesNotExist:
                if (typeof(q) != 1):
                    qu = PastQuestion(question=q, answer=a, category=t)
                    qu.save()
                pass


            return render(request, 'answer.html', {'question': q, 'answer': a, 'type': t, 'building_street': b_street, 'pastquestions':pq, 'url':urlsearch})

    return render(request, 'index.html', {'pastquestions':pq})

def test(request):
    get_all_entities()
    return HttpResponse("Saved all entities.")


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

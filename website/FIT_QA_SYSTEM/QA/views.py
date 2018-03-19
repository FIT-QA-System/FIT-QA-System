from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import re
from .models import *
from .forms import QuestionForm
from .question_answering import *
# from src.Translator import answer, typeof


def index(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['question']
            result = answer(q)
            t = typeof(q)
            a = result['answer']
            lat = None
            long = None

            if typeof(q) == 2:
                if result['answer'] == "Location not found":
                    t = 0
                else:
                    lat = result['lat']
                    long = result['long']
                    a = result['answer'].replace(" ", "+").lower()

            return render(request, 'answer.html', {'question': q, 'answer': result['answer'], 'type': t, 'lat': lat, 'long': long, 'a':a})

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

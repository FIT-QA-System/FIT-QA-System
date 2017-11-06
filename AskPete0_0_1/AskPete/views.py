from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'AskPete/index.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'AskPete/results.html', {'question': question})




def get_query(request, input_text):
    # if this is a POST request we need to process the form data
    #return HttpResponse(request)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        searchstring = SearchForm(request.POST)
        answer = Question.answer_text
        print(answer)
        return HttpResponse("good")
        # check whether it's valid:
        if form.is_valid():
            print(input_text)
            if (input_text == Question.question_text):
               print(Question.answer_text)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('/index/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'AskPete\index.html', {'form': form})

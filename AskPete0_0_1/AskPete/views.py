from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from .forms import SearchForm
from .models import Question, Answer


def index(request):
    return render(request, 'AskPete/index.html')


def results(request):
    return render(request, 'AskPete/results.html')




def get_query(request):
    # if this is a POST request we need to process the form data
    #return HttpResponse(request)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        answer = Question.answer_text
        print(answer)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('/index/')

    # if a GET (or any other method) we'll create a blank form
    else:
        #form = SearchForm()
        search_query = request.GET.get('query', None)
        # Do whatever you need with the word the user looked for
        question = Question.objects.get(question_text=search_query)
        answer = Answer.objects.get(question=question)
        return render(request, 'AskPete/results.html', {'question':question, 'answer':answer})

    return render(request, 'AskPete/index.html', {'form': form})

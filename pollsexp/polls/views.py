from django.shortcuts import render, redirect
from polls.models import Question, Choice

# Create your views here.
def home(request):
    question_list = Question.objects.all()
    return render(request, "home.html", {"question_list":question_list})

def result(request,question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "result.html",{"question":question, "choice_list":question.choice_set.all()})

def options(request,question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "options.html",{"question":question, "choice_list":question.choice_set.all()})

def vote(request, question_id):
    choice = Choice.objects.get(id=request.POST["choice_id"])
    choice.vote()
    return redirect('/polls/%s/' % (question_id))

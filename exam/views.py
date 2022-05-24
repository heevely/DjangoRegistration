from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Question, Choice

def index(request):
    question_list = Question.objects.order_by('id')[:5]
    template = loader.get_template('exam/index.html')
    context = {'question_list': question_list, }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'exam/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if question_id == 1:
        answer = 2
    elif question_id == 2:
        answer = 2
    elif question_id == 3:
        answer = 2
    elif question_id == 4:
        answer = 3
    return render(request, 'exam/results.html',
                  {'question': question, 'answer': answer})

def statistics(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'exam/statistics.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'exam/detail.html',{
            'question': question,
            'error_message': "You didn't select an answer.",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('exam:results', args=(question_id,)))

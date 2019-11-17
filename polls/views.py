from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Choice, Question

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'current_question_list'

    def get_queryset(self):
        """
        Return all questions currently polling.
        """
        return Question.objects.filter(polls_open__lte=timezone.now(),
            polls_close__gte=timezone.now()).order_by('-polls_close')

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't currently polling.
        """
        return Question.objects.filter(polls_open__lte=timezone.now(),
            polls_close__gte=timezone.now())

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if request.user in question.voters.all():
            # User has already voted
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You've already voted in this poll."
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Add this voter to the list of voters for this question
            question.voters.add(request.user)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

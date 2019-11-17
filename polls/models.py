import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_description = models.CharField(max_length=2000)
    polls_open = models.DateTimeField('polls open')
    polls_close = models.DateTimeField('polls close')
    def __str__(self):
        return self.question_text
    def is_open(self):
        now = timezone.now()
        return self.polls_open <= now <= self.polls_close
    is_open.admin_order_field = 'polls_close'
    is_open.boolean = True
    is_open.short_description = 'Polls currently open?'
    voters = models.ManyToManyField(User)
    # single_transferable_vote = models.BooleanField()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

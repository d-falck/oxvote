from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_text', 'question_description', 'polls_open', 'polls_close']
    inlines = [ChoiceInline]
    list_display = ('question_text', 'question_description', 'polls_open', 'polls_close', 'is_open')
    list_filter = ['polls_open', 'polls_close']
    search_fields = ['question_text', 'question_description']

admin.site.register(Question, QuestionAdmin)

from django.contrib import admin
from .models import Question,Choice
# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date Info', {'fields':['pub_date'], 'classes':['collapse']})
    ]
    #fields = ['pub_date', 'question_text']
    inlines = [ChoiceInLine]
    list_display=('question_text', 'pub_date', 'was_publish_recently')
    search_fields = ['question_text']
    list_filter = ['pub_date']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

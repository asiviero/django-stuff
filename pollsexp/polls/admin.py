from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]
    list_display = ("question","publication_date")

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

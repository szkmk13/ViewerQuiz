from django import forms
from django.contrib import admin
from django.forms import BaseModelFormSet, BaseInlineFormSet

from questions.models import Question, Answer, Travel, Viewer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 7


class QuestionAdminForm(forms.ModelForm):
    multiplier = forms.DecimalField(required=False)

    class Meta:
        model = Question
        fields = '__all__'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # form = QuestionAdminForm
    list_display = ('travel', 'question', 'answer',)
    inlines = [AnswerInline, ]


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_from', 'date_to')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'viewer', 'points')

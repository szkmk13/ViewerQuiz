from django.db.models import Count, Sum
from django.views.generic import TemplateView

from questions.models import Travel, Answer, Viewer, Question


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['travels'] = Travel.objects.all()
        context['viewers'] = Viewer.objects.all().annotate(total_points=Sum('answers__points')).order_by("-total_points")
        context['questions'] = Question.objects.all()
        context['base_url'] = self.request.build_absolute_uri()
        sorted_questions = []
        for question in context['questions']:
            a = {"question": question}
            sorted_points = []
            for viewer in context['viewers']:
                if question.answers.filter(viewer=viewer).exists():
                    sorted_points.append(question.answers.get(viewer=viewer).points)
                else:
                    sorted_points.append(0)
            a["points"] = sorted_points
            sorted_questions.append(a)
        context['sorted'] = sorted_questions

        return context


class TravelDetail(TemplateView):
    template_name = "details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['travels'] = Travel.objects.all()
        travel = self.kwargs['travel']
        context['base_url'] = self.request.build_absolute_uri().split(travel)[0]

        questions = Question.objects.filter(travel__description=travel)
        answers = Answer.objects.filter(question__in=questions)
        viewers = Viewer.objects.filter(answers__in=answers).distinct()
        viewers_with_points = viewers.annotate(total_points=Sum('answers__points')).order_by("-total_points")

        sorted_questions = []
        for question in questions:
            a = {"question": question}
            sorted_points = []
            for viewer in viewers_with_points:
                if question.answers.filter(viewer=viewer).exists():
                    sorted_points.append(question.answers.get(viewer=viewer).points)
                else:
                    sorted_points.append(0)
            a["points"] = sorted_points
            sorted_questions.append(a)

        context['questions'] = questions
        context['answers'] = answers
        context['viewers'] = viewers_with_points
        context['sorted'] = sorted_questions
        return context

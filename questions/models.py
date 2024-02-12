from django.db import models
from unicodedata import decimal


def guess_formula(guessed_value, answer) -> decimal:
    return -0.02 * abs(guessed_value - answer) + 1


class Viewer(models.Model):
    name = models.CharField(max_length=20)
    instagram = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Travel(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.description


class Question(models.Model):
    ABCD = 'abcd'
    GUESS = "guess"
    DESCRIPTION = "description"
    TYPE_CHOICES = ((ABCD, ABCD), (GUESS, GUESS), (DESCRIPTION, DESCRIPTION))

    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(choices=TYPE_CHOICES, max_length=20)
    question = models.TextField(null=True)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class Answer(models.Model):
    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=200)
    points = models.DecimalField(max_digits=5, decimal_places=3, blank=True)

    def __str__(self):
        return self.viewer.name + " " + self.answer

    def save(self, *args, **kwargs):
        if not self.id:
            if self.question.type == Question.ABCD:
                if self.answer == self.question.answer:
                    self.points = 1
            if self.question.type == Question.GUESS:
                answer = float(self.answer)
                correct_answer = float(self.question.answer)
                self.points = guess_formula(answer, correct_answer)
            if not self.points:
                self.points = 0
            if self.question.type == Question.DESCRIPTION:
                pass
        super().save(*args, **kwargs)

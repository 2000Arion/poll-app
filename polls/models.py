import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Frage")
    pub_date = models.DateTimeField("Veröffentlichungsdatum")

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Frage")
    choice_text = models.CharField(max_length=200, verbose_name="Antwortmöglichkeit")
    votes = models.IntegerField(default=0, verbose_name="Stimmen")

    class Meta:
        verbose_name = "Antwortmöglichkeit"
        verbose_name_plural = "Antwortmöglichkeiten"

    def __str__(self):
        return self.choice_text

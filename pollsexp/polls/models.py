from django.db import models
import datetime

# Create your models here.
class Choice(models.Model):
    text = models.TextField(default="")
    vote_count = models.IntegerField(default = 0)
    question = models.ForeignKey("Question")
    def vote(self):
        self.vote_count += 1
        self.save()

class Question(models.Model):
    question = models.TextField(default="")
    publication_date = models.DateField(default=datetime.date.today())

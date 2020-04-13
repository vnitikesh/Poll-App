from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone




# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    

class Question(models.Model):
    objects = None
    question_text = models.CharField(max_length = 200, verbose_name = "Polling question")
    pub_date = models.DateTimeField(verbose_name = "date published")


    def __str__(self):
        return self.question_text


    def was_published_recently(self):
        now = timezone.now()
        #return now - datetime.timedelta(days = 1) <= self.pub_date <= now

        return now - datetime.timedelta(days = 1) <= self.pub_date <= now


class Choice(models.Model):

    DoesNotExist = None
    choice_text = models.CharField(max_length = 200)
    vote = models.IntegerField(default = 0)
    question = models.ForeignKey(Question,on_delete = models.CASCADE)

    def __str__(self):
        return self.choice_text

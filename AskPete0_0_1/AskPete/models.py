from django.db import models

# Create your models here.
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)

    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=200)
    isAddress = models.BooleanField(default="False", name="Is Address?")


    def __str__(self):
        return self.answer_text



class CourseInfo(models.Model):
    crn = models.IntegerField()
    subject = models.CharField(max_length=8)
    section = models.CharField(max_length=3)
    credit = models.IntegerField()
    title = models.CharField
    description = models.TextField
    instructor = models.CharField(max_length=100)
    semester = models.CharField(max_length=11)
    days = models.CharField(max_length=4)
    time = models.TimeField
    place = models.CharField

from django.db import models
from django_google_maps.fields import AddressField, GeoLocationField

class Rental(models.Model):
    address = AddressField(max_length=100)

    geolocation = GeoLocationField(blank=True)

    def __str__(self):
        return self.address

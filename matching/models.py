from django.db import models


#This is the model to create our database
#We define what the fields will be and what kind of database
#will be placed in them
class User(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    major = models.CharField(max_length=100, blank=True)
    grad_year = models.CharField(max_length=4)
    bio = models.TextField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    team = models.ManyToManyField('Team', blank=True)
    match = models.ManyToManyField('User', blank=True)


class Team(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField()


class Match(models.Model):
    match_date = models.DateTimeField()

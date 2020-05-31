from django.db import models
# Create your models here.


class tblUser(models.Model):
    Name = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)


class tblAllProject(models.Model):
    ProjectName = models.CharField(max_length=300)
    Duration = models.IntegerField()
    ProjectManager = models.CharField(max_length=200)
    Description = models.CharField(max_length=500)


class tblTaskList(models.Model):
    TaskName = models.CharField(max_length=300)
    ProjectID = models.IntegerField()
    startDate = models.DateField()
    EndDate = models.DateField()
    Description = models.CharField(max_length=500)
    Assignee = models.CharField(max_length=100)

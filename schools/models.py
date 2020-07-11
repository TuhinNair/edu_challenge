from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    student_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
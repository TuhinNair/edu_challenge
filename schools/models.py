from django.db import models
import uuid

# Create your models here.

class School(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=20)
    max_student_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Student(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
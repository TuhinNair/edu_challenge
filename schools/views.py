from django.shortcuts import render
from .models import School, Student
from rest_framework import viewsets
from .serializers import SchoolSerializer, StudentSerializer
# Create your views here.

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        school = self.kwargs.get('school_pk', None)
        if school:
            return Student.objects.filter(school=school)
        return Student.objects.all()

    serializer_class =  StudentSerializer
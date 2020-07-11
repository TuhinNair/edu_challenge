from django.shortcuts import render
from .models import School, Student
from rest_framework import viewsets
from .serializers import SchoolSerializer, StudentSerializer
# Create your views here.

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class =  StudentSerializer
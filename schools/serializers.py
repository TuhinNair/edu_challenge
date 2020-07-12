from rest_framework import serializers

from .models import School, Student

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'max_student_count']

class StudentSerializer(serializers.ModelSerializer):
    def validate(self, data): 
        school =  data.get('school', None)
        if school: 
            school_limit = School.objects.get(pk=school.id).max_student_count
            students_enrolled = len(Student.objects.filter(school__id=school.id))
            #Add a GTE check because no Model level validation is in place.
            if students_enrolled >= school_limit:
                raise serializers.ValidationError('School is at max capacity')
        return data

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'school']
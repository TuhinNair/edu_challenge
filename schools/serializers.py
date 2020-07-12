from rest_framework import serializers

from .models import School, Student

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'max_student_count']

class StudentSerializer(serializers.ModelSerializer):
    def validate(self, data): 
        school_id =  data.get('school_id', None)
        if school_id: 
            school_limit = School.objects.get(pk=school_id.id).max_student_count
            students_enrolled = len(Student.objects.filter(school_id__id=school_id.id))
            #Add a GTE check because no Model level validation is in place.
            if students_enrolled >= school_limit:
                raise serializers.ValidationError('School is at max capacity')
        return data

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'school_id']
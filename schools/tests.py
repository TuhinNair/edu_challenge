from rest_framework import status
from rest_framework.test import APITestCase
from .models import School, Student
# Create your tests here.

class SchoolTest(APITestCase):
    def test_post_school(self):
        url = '/schools/'
        data = {'id': 'this should not work', 'name': 'school_foo', 'max_student_count': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual('school_foo', response.data['name'])
        self.assertEqual(100, response.data['max_student_count'])
        self.assertNotEqual('this should not work', response.data['id'])
        self.assertNotEqual('', response.data['id'])
    
    def test_get_schools(self):
        School.objects.create(name='school_foo', max_student_count=23)
        School.objects.create(name='school_bar', max_student_count=53)
        School.objects.create(name='school_foo_bar', max_student_count=253)

        url = '/schools/'
        response = self.client.get(url)
        self.assertEqual(3, len(response.data))

class StudentTest(APITestCase):
    def test_post_student(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/students/'
        data = {'id': 'this should not work', 'first_name': 'foo', 'last_name': 'bar',  'school_id': test_school.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual('foo', response.data['first_name'])
        self.assertEqual(test_school.id, response.data['school_id'])
        self.assertNotEqual('this should not work', response.data['id'])
        self.assertNotEqual('', response.data['id'])
    
    def test_get_students(self):
        test_school = School.objects.create(name='school_bar', max_student_count=23)

        Student.objects.create(first_name='fooda', last_name='bar', school_id=test_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=test_school)
        Student.objects.create(first_name='fodao', last_name='bar', school_id=test_school)

        url = '/students/'
        response = self.client.get(url)
        self.assertEqual(3, len(response.data))
    


    
        
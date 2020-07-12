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
        self.assertEqual(response.data['name'], 'school_foo')
        self.assertEqual(response.data['max_student_count'], 100)
        self.assertNotEqual(response.data['id'], 'this should not work')
        self.assertNotEqual(response.data['id'], '')
    
    def test_get_schools(self):
        School.objects.create(name='school_foo', max_student_count=23)
        School.objects.create(name='school_bar', max_student_count=53)
        School.objects.create(name='school_foo_bar', max_student_count=253)

        url = '/schools/'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_put_school(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/schools/{}/'.format(str(test_school.id))
        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_bar')
        data = {'id': test_school.id, 'name': 'school_bar', 'max_student_count': 100}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_foo')
    
    def test_patch_school(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/schools/{}/'.format(str(test_school.id))
        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_bar')
        data = {'name': 'school_bar'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_foo')

class StudentTest(APITestCase):
    def test_post_student(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/students/'
        data = {'id': 'this should not work', 'first_name': 'foo', 'last_name': 'bar',  'school_id': test_school.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(response.data['first_name'], 'foo')
        self.assertEqual(response.data['school_id'], test_school.id)
        self.assertNotEqual(response.data['id'], 'this should not work')
        self.assertNotEqual(response.data['id'], '')
    
    def test_get_students(self):
        test_school = School.objects.create(name='school_bar', max_student_count=23)

        Student.objects.create(first_name='foo', last_name='bar', school_id=test_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=test_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=test_school)

        url = '/students/'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)
    
    def test_put_students(self):
        test_school = School.objects.create(name='school_foo', max_student_count=23)

        Student.objects.create(first_name='foo', last_name='bar', school_id=test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='bar')
        data = {'id': test_student.id, 'first_name': 'bar', 'last_name': 'foo', 'school_id':test_school.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foo')
    
    def test_patch_students(self):
        test_school = School.objects.create(name='school_foo', max_student_count=23)

        Student.objects.create(first_name='foo', last_name='bar', school_id=test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='bar')
        data = {'first_name': 'bar'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foo')

        

    


    
        
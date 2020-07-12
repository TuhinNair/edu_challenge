from rest_framework import status
from rest_framework.test import APITestCase
from .models import School, Student
# Create your tests here.

class SchoolTest(APITestCase):
    def test_post_school(self):
        url = '/schools/'
        data = {'id': 'this should not be the id', 'name': 'school_foo', 'max_student_count': 100}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual(response.data['name'], 'school_foo')
        self.assertEqual(response.data['max_student_count'], 100)
        self.assertNotEqual(response.data['id'], 'this should not be the id')
        self.assertNotEqual(response.data['id'], '')
    
    def test_post_school_no_name(self):
        url = '/schools/'
        data = { 'max_student_count': 100}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_school_no_max_student_count(self):
        url = '/schools/'
        data = {'name': 'school_foo'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_school_no_id_request(self):
        url = '/schools/'
        data = {'name': 'school_foo', 'max_student_count': 100}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual(response.data['name'], 'school_foo')
        self.assertEqual(response.data['max_student_count'], 100)
        self.assertNotEqual(response.data['id'], '')
    
    def test_post_school_invalid_name_length(self):
        url = '/schools/'
        data = {'name': 'This is longer than 20 characters', 'max_student_count': 100}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_school_invalid_max_student_count(self):
        url = '/schools/'
        data = {'name': 'school_foo', 'max_student_count': -1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
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
    
    def test_put_school_no_name(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/schools/{}/'.format(str(test_school.id))

        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_bar')

        data = {'id': test_school.id, 'max_student_count': 100}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_put_school_no_student_max_count(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/schools/{}/'.format(str(test_school.id))

        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_bar')

        data = {'id': test_school.id, 'name': 'school_bar'}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_school(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')
        url = '/schools/{}/'.format(str(test_school.id))

        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_bar')

        data = {'name': 'school_bar'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(School.DoesNotExist,  School.objects.get, name='school_foo')
    
    def test_delete_school(self):
        School.objects.create(name='school_foo', max_student_count=23)
        test_school = School.objects.get(name='school_foo')

        self.assertEqual(School.objects.count(), 1)

        url = '/schools/{}/'.format(str(test_school.id))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(School.objects.count(), 0)

        
class StudentTest(APITestCase):
    def setUp(self):
        School.objects.create(name='school_foo', max_student_count=23)
        self.test_school = School.objects.get(name='school_foo')

    def test_post_student(self):
        url = '/students/'
        data = {'id': 'this should not be the id', 'first_name': 'foo', 'last_name': 'bar',  'school_id': self.test_school.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(response.data['first_name'], 'foo')
        self.assertEqual(response.data['school_id'],self. test_school.id)
        self.assertNotEqual(response.data['id'], 'this should not be the id')
        self.assertNotEqual(response.data['id'], '')
    
    def test_post_student_no_id_request(self):
        url = '/students/'
        data = {'first_name': 'foo', 'last_name': 'bar',  'school_id': self.test_school.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(response.data['first_name'], 'foo')
        self.assertEqual(response.data['school_id'],self. test_school.id)
        self.assertNotEqual(response.data['id'], '')
    
    def test_post_student_invalid_first_name(self):
        url = '/students/'
        data = {'first_name': 'This is longer than 20 characters', 'last_name': 'bar',  'school_id': self.test_school.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_student_invalid_last_name(self):
        url = '/students/'
        data = {'first_name': 'foo', 'last_name': 'This is longer than 20 characters',  'school_id': self.test_school.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_student_invalid_school_id(self):
        url = '/students/'
        data = {'first_name': 'foo', 'last_name': 'This is longer than 20 characters',  'school_id': 'invalid_school_id'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_student_no_first_name(self):
        url = '/students/'
        data = {'last_name': 'bar',  'school_id': self.test_school.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_student_no_last_name(self):
        url = '/students/'
        data = {'first_name': 'foo',  'school_id': self.test_school.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_student_no_school_id(self):
        url = '/students/'
        data = {'first_name': 'foo',  'last_name': 'foo'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_students(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        url = '/students/'
        response = self.client.get(url)

        self.assertEqual(len(response.data), 3)
    
    def test_put_students(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))

        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='bar')
        
        data = {'id': test_student.id, 'first_name': 'bar', 'last_name': 'foo', 'school_id':self.test_school.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foo')
    
    def test_put_students_no_first_name(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))

        data = {'id': test_student.id, 'last_name': 'foo', 'school_id':self.test_school.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_put_students_no_last_name(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))

        data = {'id': test_student.id, 'first_name': 'bar', 'school_id':self.test_school.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_put_students_no_school_id(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))

        data = {'id': test_student.id, 'first_name': 'bar', 'last_name': 'foo'}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_students(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))

        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='bar')

        data = {'first_name': 'bar'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foo')
    
    def test_delete_student(self):
        Student.objects.create(first_name='foo', last_name='bar', school_id=self.test_school)
        test_student = Student.objects.get(first_name='foo')
        url = '/students/{}/'.format(str(test_student.id))

        self.assertEqual(Student.objects.count(), 1)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
    
    def test_post_student_over_school_limit(self):
        School.objects.create(name='school_bar', max_student_count=2)
        max_two_school = School.objects.get(name='school_bar')
        Student.objects.create(first_name='foo', last_name='bar', school_id=max_two_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=max_two_school)

        url = '/students/'
        data = {'first_name': 'foo', 'last_name': 'bar',  'school_id': max_two_school.id}
        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_put_student_over_school_limit(self):
        School.objects.create(name='school_bar', max_student_count=2)
        max_two_school = School.objects.get(name='school_bar')
        Student.objects.create(first_name='foo', last_name='bar', school_id=max_two_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=max_two_school)

        Student.objects.create(first_name='bar', last_name='foo', school_id=self.test_school)
        test_student = Student.objects.get(first_name='bar')
        
        url = '/students/{}/'.format(str(test_student.id))
        data = {'first_name': 'bar', 'last_name': 'foo',  'school_id': max_two_school.id}
        response = self.client.put(url, data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patch_student_over_school_limit(self):
        School.objects.create(name='school_bar', max_student_count=2)
        max_two_school = School.objects.get(name='school_bar')
        Student.objects.create(first_name='foo', last_name='bar', school_id=max_two_school)
        Student.objects.create(first_name='foo', last_name='bar', school_id=max_two_school)

        Student.objects.create(first_name='bar', last_name='foo', school_id=self.test_school)
        test_student = Student.objects.get(first_name='bar')
        
        url = '/students/{}/'.format(str(test_student.id))
        data = {'school_id': max_two_school.id}
        response = self.client.patch(url, data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)




        

    


    
        
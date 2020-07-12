from rest_framework import status
from rest_framework.test import APITestCase
from schools.models import School, Student

class SchoolHasStudentTest(APITestCase):
    def setUp(self):
        School.objects.create(name='school_foo', max_student_count=20)
        School.objects.create(name='school_bar', max_student_count=2)
        self.test_school_1 = School.objects.get(name='school_foo')
        self.test_school_2 = School.objects.get(name='school_bar')

        Student.objects.create(first_name='foo', last_name='bar', school=self.test_school_1)
        Student.objects.create(first_name='bar', last_name='foo', school=self.test_school_2)
        self.test_student_1 = Student.objects.get(first_name='foo')
        self.test_student_2 = Student.objects.get(first_name='bar')
    
    def test_get_all_students_of_school(self):
        Student.objects.create(first_name='bar_foo', last_name='foo_bar', school=self.test_school_1)

        url = '/schools/{}/students/'.format(str(self.test_school_1.id))
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
    
    def test_get_student_instance_of_school(self):
        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_1.id))
        response = self.client.get(url)
        expected = {'id': str(self.test_student_1.id), 'first_name':'foo', 'last_name':'bar', 'school': self.test_school_1.id }
        self.assertEqual(response.data, expected)
    
    def test_post_student_instance_of_school(self):
        url = '/schools/{}/students/'.format(str(self.test_school_1.id))
        data = {'first_name': 'foo', 'last_name': 'bar',  'school': self.test_school_1.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'foo')
        self.assertEqual(response.data['school'],self. test_school_1.id)
        self.assertNotEqual(response.data['id'], '')
    
    def test_put_student_instance_of_school(self):
        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_1.id))
        data = {'id': str(self.test_student_1.id), 'first_name': 'foobar', 'last_name': 'bar',  'school': self.test_school_1.id}

        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foobar')

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foo')
    
    def test_patch_student_instance_of_school(self):
        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_1.id))
        data = {'first_name': 'foobar'}

        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foobar')

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Student.DoesNotExist,  Student.objects.get, first_name='foo')
    
    def test_get_non_existent_student_instance_of_school(self):
        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_2.id))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def test_post_invalid_invariant_max_student_count(self):
        Student.objects.create(first_name='bar_foo', last_name='foo_bar', school=self.test_school_2)
        self.assertEqual(len(Student.objects.filter(school__id=self.test_school_2.id)), 2)

        url = '/schools/{}/students/'.format(str(self.test_school_2.id))
        data = {'first_name': 'foobar', 'last_name': 'barfoo',  'school': self.test_school_2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_put_invalid_invariant_max_student_count(self):
        Student.objects.create(first_name='bar_foo', last_name='foo_bar', school=self.test_school_2)
        self.assertEqual(len(Student.objects.filter(school__id=self.test_school_2.id)), 2)

        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_1.id))
        data = {'id': str(self.test_student_1.id), 'first_name': 'foobar', 'last_name': 'bar',  'school': self.test_school_2.id}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_invalid_invariant_max_student_count(self):
        Student.objects.create(first_name='bar_foo', last_name='foo_bar', school=self.test_school_2)
        self.assertEqual(len(Student.objects.filter(school__id=self.test_school_2.id)), 2)

        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_1.id))
        data = {'school': self.test_school_2.id}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_put_invalid_id_student_instance_of_school(self):
        url = '/schools/{}/students/{}/'.format(str(self.test_school_1.id), str(self.test_student_1.id))

        data = {'id': '3c1641f1-ecf8-45e0-9b55-cba273e0088c', 'first_name': 'foobar', 'last_name': 'bar',  'school': self.test_school_1.id}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'foobar')
        self.assertNotEqual(response.data['id'], '3c1641f1-ecf8-45e0-9b55-cba273e0088c')
        self.assertNotEqual(response.data['id'], self.test_student_1.id)



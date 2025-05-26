from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from .models import Section, Test, TestResult


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создание пользователей
        self.teacher = CustomUser.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='TeacherPass123',
            role='teacher'
        )
        self.student = CustomUser.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='StudentPass123',
            role='student'
        )

        # Создание раздела и теста
        self.section = Section.objects.create(
            title='Test Section',
            description='Test Description',
            created_by=self.teacher
        )
        self.test = Test.objects.create(
            title='Test Title',
            section=self.section,
            created_by=self.teacher
        )

        # Получение токенов
        self.teacher_token = self.get_token('teacher1', 'TeacherPass123')
        self.student_token = self.get_token('student1', 'StudentPass123')

    def get_token(self, username, password):
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password
        })
        return response.data['access']

    def test_get_sections(self):
        response = self.client.get('/api/sections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Section')

    def test_create_section_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post('/api/sections/', {
            'title': 'New Section',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 2)

    def test_create_section_student(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/sections/', {
            'title': 'New Section',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tests_by_section(self):
        response = self.client.get(f'/api/tests/?section={self.section.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Title')

    def test_create_test_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post('/api/tests/', {
            'title': 'New Test',
            'section': self.section.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), 2)

    def test_create_test_student(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/tests/', {
            'title': 'New Test',
            'section': self.section.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_test_result_student(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/test-results/', {
            'test': self.test.id,
            'answer': 'Sample answer',
            'score': 85
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestResult.objects.count(), 1)

    def test_create_test_result_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post('/api/test-results/', {
            'test': self.test.id,
            'answer': 'Teacher answer',
            'score': 90
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestResult.objects.count(), 1)

    def test_update_section_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.patch(f'/api/sections/{self.section.id}/', {
            'title': 'Updated Section'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.section.refresh_from_db()
        self.assertEqual(self.section.title, 'Updated Section')

    def test_delete_section_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.delete(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Section.objects.count(), 0)

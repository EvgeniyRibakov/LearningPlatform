from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from .models import Section, Test, TestResult, Material, Question
from LearningPlatform.tasks import send_test_result_notification


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создание пользователей
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123'
        )
        self.teacher = CustomUser.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='TeacherPass123',
            role='teacher'
        )
        self.teacher2 = CustomUser.objects.create_user(
            username='teacher2',
            email='teacher2@example.com',
            password='Teacher2Pass123',
            role='teacher'
        )
        self.student = CustomUser.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='StudentPass123',
            role='student'
        )

        # Создание раздела, материала, теста и вопроса
        self.section = Section.objects.create(
            title='Test Section',
            description='Test Description',
            created_by=self.teacher
        )
        self.material = Material.objects.create(
            title='Test Material',
            content='Sample content',
            section=self.section,
            created_by=self.teacher
        )
        self.test = Test.objects.create(
            title='Test Title',
            section=self.section,
            material=self.material,
            created_by=self.teacher
        )
        self.question = Question.objects.create(
            test=self.test,
            text='What is 2+2?',
            correct_answer='4'
        )
        self.test_result = TestResult.objects.create(
            test=self.test,
            student=self.student,
            answer='Sample answer',
            score=85
        )

        # Получение токенов
        self.admin_token = self.get_token('admin', 'AdminPass123')
        self.teacher_token = self.get_token('teacher1', 'TeacherPass123')
        self.teacher2_token = self.get_token('teacher2', 'Teacher2Pass123')
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

    def test_get_materials(self):
        response = self.client.get('/api/materials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Material')

    def test_create_material_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post('/api/materials/', {
            'title': 'New Material',
            'content': 'New content',
            'section': self.section.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Material.objects.count(), 2)

    def test_create_material_student(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/materials/', {
            'title': 'New Material',
            'content': 'New content',
            'section': self.section.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tests_by_section(self):
        response = self.client.get(f'/api/tests/?section={self.section.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Title')

    def test_get_tests_by_material(self):
        response = self.client.get(f'/api/tests/?material={self.material.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Title')

    def test_create_test_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post('/api/tests/', {
            'title': 'New Test',
            'section': self.section.id,
            'material': self.material.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), 2)

    def test_create_test_student(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/tests/', {
            'title': 'New Test',
            'section': self.section.id,
            'material': self.material.id
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
        self.assertEqual(TestResult.objects.count(), 2)

    def test_create_test_result_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.post('/api/test-results/', {
            'test': self.test.id,
            'answer': 'Teacher answer',
            'score': 90
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestResult.objects.count(), 2)

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

    def test_check_answer_correct(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/check-answer/', {
            'question_id': self.question.id,
            'answer': '4'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_correct'])
        self.assertEqual(response.data['score'], 100)
        self.assertEqual(TestResult.objects.count(), 2)

    def test_check_answer_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post('/api/check-answer/', {
            'question_id': self.question.id,
            'answer': '5'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_correct'])
        self.assertEqual(response.data['score'], 0)
        self.assertEqual(TestResult.objects.count(), 2)

    def test_send_test_result_notification_success(self):
        result = send_test_result_notification(self.test_result.id)
        self.assertEqual(result, f"Notification sent for TestResult {self.test_result.id}")

    def test_send_test_result_notification_not_found(self):
        result = send_test_result_notification(999)
        self.assertEqual(result, "TestResult 999 not found")

    def test_update_section_other_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher2_token}')
        response = self.client.patch(f'/api/sections/{self.section.id}/', {
            'title': 'Unauthorized Update'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_test_result_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/test-results/{self.test_result.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        self.client.credentials()  # Без токена
        response = self.client.post('/api/sections/', {
            'title': 'New Section',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

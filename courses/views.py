from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Section, Test, TestResult
from .serializers import SectionSerializer, TestSerializer, TestResultSerializer
from .permissions import IsTeacherOrReadOnly, IsOwnerOrTeacher, IsStudentOrTeacher
from LearningPlatform.tasks import send_test_result_notification


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsTeacherOrReadOnly, IsOwnerOrTeacher]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsTeacherOrReadOnly, IsOwnerOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsStudentOrTeacher, IsOwnerOrTeacher]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        send_test_result_notification.delay(serializer.instance.id)

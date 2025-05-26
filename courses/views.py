from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Section, Test, TestResult, Material, Question
from .serializers import SectionSerializer, TestSerializer, TestResultSerializer, MaterialSerializer, \
    TestAnswerSerializer
from .permissions import IsTeacherOrReadOnly, IsOwnerOrTeacher, IsStudentOrTeacher
from LearningPlatform.tasks import send_test_result_notification


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsTeacherOrReadOnly, IsOwnerOrTeacher]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsTeacherOrReadOnly, IsOwnerOrTeacher]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsTeacherOrReadOnly, IsOwnerOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section', 'material']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsStudentOrTeacher, IsOwnerOrTeacher]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        send_test_result_notification.delay(serializer.instance.id)


class CheckAnswerView(APIView):
    def post(self, request):
        serializer = TestAnswerSerializer(data=request.data)
        if serializer.is_valid():
            question = Question.objects.get(id=serializer.validated_data['question_id'])
            is_correct = question.correct_answer == serializer.validated_data['answer']
            score = 100 if is_correct else 0
            TestResult.objects.create(
                test=question.test,
                student=request.user,
                answer=serializer.validated_data['answer'],
                score=score
            )
            return Response({'is_correct': is_correct, 'score': score}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

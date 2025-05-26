from rest_framework import serializers
from .models import Section, Test, TestResult, Material, Question
from users.models import CustomUser


class SectionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class MaterialSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = Material
        fields = ['id', 'title', 'content', 'section', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TestSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'section', 'material', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TestResultSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'test', 'student', 'answer', 'score', 'created_at']
        read_only_fields = ['student']


class TestAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()

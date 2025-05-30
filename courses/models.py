from django.db import models
from users.models import CustomUser


class Section(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Material(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='materials')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='materials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='tests')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='test_results')
    answer = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.test.title} by {self.student.username}"

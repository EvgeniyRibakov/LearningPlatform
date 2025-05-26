from rest_framework import permissions
from .models import Section, Test, TestResult


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsOwnerOrTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Section) or isinstance(obj, Test):
            return request.user.is_authenticated and (
                    request.user.role == 'teacher' and obj.created_by == request.user
            )
        if isinstance(obj, TestResult):
            return request.user.is_authenticated and (
                    request.user.role == 'teacher' or obj.student == request.user
            )
        return False


class IsStudentOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['student', 'teacher']

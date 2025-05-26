from django.contrib import admin
from .models import Section, Test, TestResult


admin.site.register(Section)
admin.site.register(Test)
admin.site.register(TestResult)
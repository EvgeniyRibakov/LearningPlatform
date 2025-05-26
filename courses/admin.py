from django.contrib import admin
from .models import Section, Test, TestResult, Material, Question

admin.site.register(Section)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Material)
admin.site.register(Question)

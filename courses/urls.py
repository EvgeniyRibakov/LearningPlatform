from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectionViewSet, TestViewSet, TestResultViewSet, MaterialViewSet

router = DefaultRouter()
router.register(r'sections', SectionViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'tests', TestViewSet)
router.register(r'test-results', TestResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

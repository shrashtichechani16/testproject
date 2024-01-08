from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (StudentViewSet,CSVFileUploadViewSet)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register('csv_file_upload', CSVFileUploadViewSet, basename='csv_file_upload')

urlpatterns = [
    path('', include(router.urls)),
]

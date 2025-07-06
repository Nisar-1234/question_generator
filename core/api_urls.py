from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'files', views.UploadedFileViewSet)
router.register(r'questions', views.GeneratedQuestionViewSet, basename='questions')
router.register(r'tasks', views.TaskResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-questions/', views.generate_questions_api, name='generate_questions_api'),
    path('task-status/<str:task_id>/', views.get_task_status_api, name='task_status_api'),
]

# # # core/urls.py - Complete version
# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     # Main pages
# #     path('', views.HomeView.as_view(), name='home'),
# #     path('upload/', views.upload_file, name='upload'),
# #     path('generate/<uuid:file_id>/', views.generate_questions_view, name='generate'),
# #     path('task/<str:task_id>/', views.task_status_view, name='task_status'),
# #     path('results/<uuid:file_id>/', views.results_view, name='results'),
# #     path('chat/<uuid:file_id>/', views.chat_view, name='chat'),
# #     path('export/<uuid:file_id>/pdf/', views.export_questions_pdf, name='export_pdf'),
# #     path('export/<uuid:file_id>/json/', views.export_questions_json, name='export_json'),
# #     path('export/<uuid:file_id>/csv/', views.export_questions_csv, name='export_csv'),
# #     path('export/all/', views.export_all_questions, name='export_all'),
# #     #path('api/chat/<uuid:file_id>/', views.chat_with_document, name='chat_api'),

    
# #     # API endpoints
# #     path('api/generate-questions/', views.generate_questions_api, name='generate_questions_api'),
# #     path('api/task-status/<str:task_id>/', views.get_task_status_api, name='task_status_api'),
# #     #path('api/chat/<uuid:file_id>/', views.chat_with_document, name='chat_api'),
# # ]






# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.HomeView.as_view(), name='home'),
#     path('upload/', views.upload_file, name='upload'),
#     path('generate/<uuid:file_id>/', views.generate_questions_view, name='generate'),
#     path('task/<str:task_id>/', views.task_status_view, name='task_status'),
#     path('results/<uuid:file_id>/', views.results_view, name='results'),
#     path('chat/<uuid:file_id>/', views.chat_view, name='chat'),
    
#     # Export specific file questions
#     path('export/<uuid:file_id>/pdf/', views.export_questions_pdf, name='export_pdf'),
#     path('export/<uuid:file_id>/docx/', views.export_questions_docx, name='export_docx'),
#     path('export/<uuid:file_id>/txt/', views.export_questions_txt, name='export_txt'),
#     path('export/<uuid:file_id>/json/', views.export_questions_json, name='export_json'),
#     path('export/<uuid:file_id>/csv/', views.export_questions_csv, name='export_csv'),
    
#     # Export ALL questions
#     path('export/all/pdf/', views.export_all_questions_pdf, name='export_all_pdf'),
#     path('export/all/docx/', views.export_all_questions_docx, name='export_all_docx'),
#     path('export/all/txt/', views.export_all_questions_txt, name='export_all_txt'),
#     path('export/all/json/', views.export_all_questions_json, name='export_all_json'),
#     path('export/all/csv/', views.export_all_questions_csv, name='export_all_csv'),
# ]




from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('generate/<uuid:file_id>/', views.generate_questions_view, name='generate'),
    path('task/<str:task_id>/', views.task_status_view, name='task_status'),
    path('results/<uuid:file_id>/', views.results_view, name='results'),
    path('chat/<uuid:file_id>/', views.chat_view, name='chat'),
    
    # Add the missing chat API endpoint
    path('api/chat/<uuid:file_id>/', views.chat_with_document, name='chat_api'),
    
    # Export specific file questions
    path('export/<uuid:file_id>/pdf/', views.export_questions_pdf, name='export_pdf'),
    path('export/<uuid:file_id>/docx/', views.export_questions_docx, name='export_docx'),
    path('export/<uuid:file_id>/txt/', views.export_questions_txt, name='export_txt'),
    path('export/<uuid:file_id>/json/', views.export_questions_json, name='export_json'),
    path('export/<uuid:file_id>/csv/', views.export_questions_csv, name='export_csv'),
    
    # Export ALL questions
    path('export/all/pdf/', views.export_all_questions_pdf, name='export_all_pdf'),
    path('export/all/docx/', views.export_all_questions_docx, name='export_all_docx'),
    path('export/all/txt/', views.export_all_questions_txt, name='export_all_txt'),
    path('export/all/json/', views.export_all_questions_json, name='export_all_json'),
    path('export/all/csv/', views.export_all_questions_csv, name='export_all_csv'),
    path('debug/test-ai/', views.test_ai_integration, name='test_ai'),
    path('debug/ai-status/', views.check_ai_status, name='ai_status'),
]

# # question_generator/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('core.urls')),
#     path('api/', include('core.api_urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # # core/urls.py
# # from django.urls import path
# # #from . import views

# # urlpatterns = [
# #     path('', views.HomeView.as_view(), name='home'),
# #     path('upload/', views.upload_file, name='upload'),
# #     path('generate/<uuid:file_id>/', views.generate_questions_view, name='generate'),
# #     path('task/<str:task_id>/', views.task_status_view, name='task_status'),
# #     path('results/<uuid:file_id>/', views.results_view, name='results'),
# #     path('chat/<uuid:file_id>/', views.chat_view, name='chat'),
# # ]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # path('api/', include('core.api_urls')),  # Comment this out for now
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
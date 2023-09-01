from django.urls import path, include

from Loader import views

urlpatterns = [
    path('index', views.progress_view),
    path('celery-progress/', include('celery_progress.urls')),
]

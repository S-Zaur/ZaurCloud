from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('otp/', views.otp_verify_view, name='otp'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('social/', include('social.apps.django_app.urls', namespace='social')),
]

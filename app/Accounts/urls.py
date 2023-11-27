from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('otp/', views.otp_verify_view, name='otp'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]

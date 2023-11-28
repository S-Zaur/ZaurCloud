from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('register-complete/<int:user_id>', views.registration_complete, name='register-complete'),
    path('otp/', views.otp_verify_view, name='otp'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('social/', include('social_django.urls', namespace='social')),
]

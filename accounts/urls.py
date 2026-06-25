from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('verify/', views.verification_submit_view, name='verification_submit'),
    path('verify/status/', views.verification_status_view, name='verification_status'),
]
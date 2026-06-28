from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_pk>/', views.flag_event, name='flag_event'),
    path('admin/flags/', views.flag_list, name='flag_list'),
    path('admin/flags/<int:flag_pk>/review/', views.review_flag, name='review_flag'),
]   
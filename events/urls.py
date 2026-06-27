from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list_view, name='event_list'),
    path('<int:pk>/', views.event_detail_view, name='event_detail'),
    path('create/', views.event_create_view, name='event_create'),
    path('<int:pk>/edit/', views.event_edit_view, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete_view, name='event_delete'),
    path('<int:pk>/update/', views.event_update_post_view, name='event_update_post'),
    path('dashboard/', views.organiser_dashboard_view, name='organiser_dashboard'),
]
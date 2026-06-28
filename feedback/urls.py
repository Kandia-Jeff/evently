from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_pk>/leave/', views.leave_feedback, name='leave_feedback'),
    path('event/<int:event_pk>/', views.event_feedback, name='event_feedback'),
]
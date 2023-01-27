
from django.urls import path
from notes import views

urlpatterns = [
    path('notes/', views.notes_list),
    path('users/', views.users_list),
    path('users/<int:pk>/', views.user_detail),
]

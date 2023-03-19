
from django.urls import path
from notes import views
from rest_framework.authtoken import views as av

urlpatterns = [
    path('notes/', views.notes_list),
    path('users/', views.users_list),
    path('notes/labels/', views.labels_list),
    path('users/<int:pk>/', views.user_detail),
    path('notes/<int:pk>/', views.note_detail),
    path('notes/api-token-auth/', av.obtain_auth_token),
    path('users/register/',views.register_user)
]

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.custom_logout, name='logout'),
] 
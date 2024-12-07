from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from school import views  # Импорт views из приложения school

# Главная страница
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('admin/', admin.site.urls),  # Админка
    path('api-auth/', include('rest_framework.urls')),  # Включение DRF панели аутентификации
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),  # Регистрация
    path('profile/', views.profile, name='profile'),  # Личный кабинет
    path('courses/', include('school.urls')),  # Подключение маршрутов приложения `school` без дополнительного префикса
]

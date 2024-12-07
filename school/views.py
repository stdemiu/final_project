from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer


# API ViewSets for Course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# Course List View
@login_required
def course_list(request):
    courses = Course.objects.all()
    user_enrollments = {course.id for course in request.user.courses.all()}
    return render(request, 'school/course_list.html', {
        'courses': courses,
        'user_enrollments': user_enrollments
    })


# Course Detail View
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'school/course_detail.html', {'course': course})


# Enroll in a Course
@login_required
def enroll_in_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        if course.students.filter(id=request.user.id).exists():
            messages.warning(request, "Вы уже записаны на этот курс.")
        else:
            course.students.add(request.user)
            messages.success(request, f"Вы успешно записались на курс {course.name}.")
        return redirect(request.META.get('HTTP_REFERER', 'profile'))  # Вернуться на ту же страницу


# Unenroll from a Course
@login_required
def unenroll_from_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        if course.students.filter(id=request.user.id).exists():
            course.students.remove(request.user)
            messages.success(request, f"Вы успешно отчислились с курса {course.name}.")
        else:
            messages.warning(request, "Вы не записаны на этот курс.")
        return redirect(request.META.get('HTTP_REFERER', 'profile'))  # Вернуться на ту же страницу


# Register a User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} создан. Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# User Profile View
@login_required
def profile(request):
    user_courses = request.user.courses.all()  # Курсы, на которые записан пользователь
    all_courses = Course.objects.exclude(students=request.user)  # Курсы, на которые пользователь не записан
    return render(request, 'profile.html', {
        'user_courses': user_courses,
        'all_courses': all_courses
    })


# Custom Logout View
def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')  # Перенаправляем на главную страницу

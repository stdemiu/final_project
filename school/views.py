# Импорты
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from urllib.parse import urlparse

# Модели и формы
from .models import Course, Enrollment, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


@login_required
def course_list(request):
    # Фильтрация по запросу
    search_query = request.GET.get('search', '')
    direction_filter = request.GET.get('direction', '')
    sort_option = request.GET.get('sort', '')

    # Базовый QuerySet
    courses = Course.objects.all()

    # Поиск по названию
    if search_query:
        courses = courses.filter(name__icontains=search_query)

    # Фильтр по направлению
    if direction_filter:
        courses = courses.filter(direction=direction_filter)

    # Сортировка по цене
    if sort_option == 'price_asc':
        courses = courses.order_by('price')
    elif sort_option == 'price_desc':
        courses = courses.order_by('-price')

    # Список уникальных направлений для фильтра
    directions = Course.objects.values_list('direction', flat=True).distinct()

    # Записанные курсы пользователя
    user_enrollments = set(Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True))

    return render(request, 'school/course_list.html', {
        'courses': courses,
        'directions': directions,
        'user_enrollments': user_enrollments,
    })


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'school/course_detail.html', {'course': course})


@login_required
def enroll_in_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            messages.warning(request, "Вы уже записаны на этот курс.")
        else:
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f"Вы успешно записались на курс {course.name}.")

    # Определяем, откуда пришел пользователь
    referer_url = request.META.get('HTTP_REFERER')  # URL предыдущей страницы
    if referer_url:
        parsed_url = urlparse(referer_url).path
        if 'profile' in parsed_url:  # Если предыдущий URL содержит 'profile'
            return redirect('profile')
        elif 'courses' in parsed_url:  # Если предыдущий URL содержит 'courses'
            return redirect('course_list')

    # Если определить нельзя, по умолчанию отправляем на курсы
    return redirect('course_list')



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


@login_required
def profile(request):
    user_courses = request.user.course_enrollments.all()  # Используем updated `related_name`
    all_courses = Course.objects.exclude(id__in=[enrollment.course.id for enrollment in user_courses])  # Курсы, на которые пользователь не записан
    return render(request, 'profile.html', {
        'user_courses': [enrollment.course for enrollment in user_courses],
        'all_courses': all_courses
    })



def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')  # Перенаправляем на главную страницу



@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'school/course_detail.html', {'course': course})



@login_required
def profile_view(request):
    # Получаем или создаем профиль пользователя
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Получаем курсы пользователя и доступные курсы
    user_courses = Enrollment.objects.filter(user=request.user)
    all_courses = Course.objects.exclude(id__in=[enrollment.course.id for enrollment in user_courses])

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль успешно обновлен.")
            return redirect('profile')  # Возвращаемся на страницу профиля
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'school/profile.html', {
        'form': form,
        'user_courses': [enrollment.course for enrollment in user_courses],
        'all_courses': all_courses,
    })



# Проверка, является ли пользователь администратором
def is_admin(user):
    return user.is_staff

# Страница редактирования пользователей
@login_required
@user_passes_test(is_admin)
def edit_users(request):
    search_query = request.GET.get('search', '')  # Получаем строку поиска из GET-запроса
    if search_query:
        users = User.objects.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        ).distinct()
    else:
        users = User.objects.all()

    return render(request, 'school/edit_users.html', {
        'users': users,
        'search_query': search_query,
    })

# Удаление записи о зачислении
@user_passes_test(is_admin)
def remove_enrollment(request, user_id, course_id):
    enrollment = get_object_or_404(Enrollment, user_id=user_id, course_id=course_id)
    enrollment.delete()
    return redirect('edit_users')



def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('profile')  # Измените на URL вашей главной страницы
        else:  # Регистрация
            register_form = CustomUserCreationForm(data=request.POST)
            if register_form.is_valid():
                register_form.save()
                return redirect('login')  # Перенаправляем после успешной регистрации
    else:
        login_form = AuthenticationForm()
        register_form = CustomUserCreationForm()

    return render(request, 'registration.html', {
        'form': login_form,
        'register_form': register_form,
    })

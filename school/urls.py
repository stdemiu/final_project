from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_in_course, name='enroll'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_from_course, name='unenroll'),
    path('profile/', views.profile, name='profile'),
]

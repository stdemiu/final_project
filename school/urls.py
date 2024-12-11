from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/edit-users/', views.edit_users, name='edit_users'),
    path('', views.course_list, name='course_list'),
    path('admin/remove-enrollment/<int:user_id>/<int:course_id>/', views.remove_enrollment, name='remove_enrollment'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_in_course, name='enroll'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_from_course, name='unenroll'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_view, name='edit_profile'),
    
    
]

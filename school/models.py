from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    direction = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    teacher = models.CharField(max_length=200)
    format = models.CharField(max_length=200)
    details = models.TextField()
    students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')


    class Meta:
        db_table = 'school_courses'  # Явно укажите имя таблицы

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')


# school/models.py

from django.contrib.auth.models import User
from django.db import models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    city = models.CharField(
        max_length=100,
        choices=[
            ("Алматы", "Алматы"),
            ("Астана", "Астана"),
            ("Шымкент", "Шымкент"),
            ("Караганда", "Караганда"),
            ("Актау", "Актау"),
        ],
        verbose_name="Город"
    )
    email = models.EmailField(unique=True, verbose_name="Почта")
    gender = models.CharField(
        max_length=10,
        choices=[("Мужской", "Мужской"), ("Женский", "Женский")],
        verbose_name="Пол"
    )

    def __str__(self):
        return self.user.username
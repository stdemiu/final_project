from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    direction = models.CharField(max_length=200)  # Поле направления
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(User, related_name='courses', blank=True)

    class Meta:
        db_table = 'school_courses'  # Явно укажите имя таблицы



    def __str__(self):
        return self.name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Уникальная запись для пользователя и курса

    def __str__(self):
        return f"{self.user.username} -> {self.course.name}"

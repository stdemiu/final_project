from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import UserProfile



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'birth_date', 'city', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',  # Увеличение ширины
                'placeholder': 'Введите ваше полное имя'
            }),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }



class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма регистрации пользователя с пользовательскими описаниями полей.
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': _('Имя пользователя'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }
        help_texts = {
            'username': _('Обязательное поле. Не более 150 символов. Используйте только буквы, цифры и символы @/./+/-/_.'),
            'password1': _(
                '• Ваш пароль должен содержать как минимум 8 символов.<br>'
                '• Пароль не должен быть слишком похож на вашу личную информацию.<br>'
                '• Пароль не должен быть распространённым.<br>'
                '• Пароль не должен состоять только из цифр.'
            ),
            'password2': _('Введите тот же пароль ещё раз для подтверждения.'),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомная форма для входа.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        }),
        label=_('Имя пользователя'),
        max_length=150,
        help_text=_('Введите зарегистрированное имя пользователя.'),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }),
        label=_('Пароль'),
        help_text=_('Введите ваш пароль.'),
    )




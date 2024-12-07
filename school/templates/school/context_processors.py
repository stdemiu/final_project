# school/context_processors.py

def user_context(request):
    """Добавляет информацию о пользователе в контекст"""
    return {
        'user': request.user,  # Передаем текущего пользователя
    }

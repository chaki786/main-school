from django import template
from django.urls import reverse

from polls.models import ThreadModel

register = template.Library()

@register.filter
def display_user(user):
    if hasattr(user, 'teacher') and user.teacher:
        try:
            thread_model = ThreadModel.objects.get(sender=user)
            url = reverse('teacher:profile', args=[user.teacher.id])
            return f'{user}'
        except ThreadModel.DoesNotExist:
            return str(user)
    elif hasattr(user, 'student') and user.student:
        try:
            thread_model = ThreadModel.objects.get(sender=user)
            url = reverse('student:profile', args=[user.student.id])
            return f'{user}'
        except ThreadModel.DoesNotExist:
            return str(user)
    elif hasattr(user, 'principal') and user.principal:
        try:
            thread_model = ThreadModel.objects.get(sender=user)
            url = reverse('hod:profile', args=[user.principal.id])
            return f'{user}'
        except ThreadModel.DoesNotExist:
            return str(user)
    else:
        return str(user)

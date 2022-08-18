from django import template
from users.models import Notification

register = template.Library()

@register.filter
def notification(user):
  if user.is_authenticated:
    notifications = Notification.objects.filter(owner=user, read=False)
    if notifications.exists():
      return notifications.count()
  return 0
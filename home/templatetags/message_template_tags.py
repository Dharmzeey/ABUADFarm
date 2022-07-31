from django import template
from users.models import Messages

register = template.Library()

@register.filter
def message_count(user):
  if user.is_authenticated:
    messages = Messages.objects.filter(owner=user, read=False)
    if messages.exists():
      return messages.count()
  return 0
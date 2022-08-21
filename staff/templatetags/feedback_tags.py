from django import template
from users.models import Goods

register = template.Library()

@register.filter
def feedback(user):
  if user.is_authenticated:
    feedbacks = Goods.objects.filter(feedback_read=False, feedback__isnull=False)
    if feedbacks.exists():
      return feedbacks.count()
  return 0
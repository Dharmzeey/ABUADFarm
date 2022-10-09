import django_extensions
from users.models import Goods

def run():
  goods = Goods.objects.all()
  for i in goods:
    i.save()
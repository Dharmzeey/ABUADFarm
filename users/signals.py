from django.db.models.signals import post_save
from .models import Profile
from django.contrib.auth.models import User

def create_customer(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(owner=instance)


post_save.connect(create_customer, sender=User)
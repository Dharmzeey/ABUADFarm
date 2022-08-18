from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profile, Notification, Goods


def create_customer(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(owner=instance)


post_save.connect(create_customer, sender=User)

def create_notification(sender, instance, created, **kwargs):
  if created:
    Notification.objects.create(
      owner = instance.owner,
      product = instance,
      message = f'Dear {instance.owner} your purchase of {instance.item} has been recorded, we hope you enjoy it. \n \n Thanks for your patronage.'
    )
    
post_save.connect(create_notification, sender=Goods)
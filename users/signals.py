from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Profile, Notification, Goods


def create_customer(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(owner=instance)
post_save.connect(create_customer, sender=User)

def create_notification(sender, instance, created, **kwargs):
  if created:
    Notification.objects.create(
      owner = instance.owner,
      good = instance,
    )
post_save.connect(create_notification, sender=Goods)

# THIS HANDLES THE FUNCTIONALITY WHEN USER UPDATE THE PROFILE, THE USER MODEL(FIRST AND LAST NAME) WILL BE MODIFIED ALSO
def update_user_model(sender, instance, created, **kwargs):
  if not created:
    get_user = User.objects.get(username=instance.owner.username)
    get_user.first_name = instance.first_name
    get_user.last_name = instance.last_name
    get_user.save()
post_save.connect(update_user_model, sender=Profile)


def create_slug(sender, created, instance, **kwargs):
  if created:
    slug_input = f"{instance.quantity}-Kg-of-{instance.item}-purchase-{instance.id}"
    instance.slug = slugify(slug_input)
    instance.save()
post_save.connect(create_slug, sender=Goods)

# HERE IF I USE IT IT WILL CAUSE THE USER AND PROFILE MODEL TO RECURSE
# def update_profile_model(sender, instance, created, **kwargs):
#   if not created:
#     get_profile = Profile.objects.get(owner=instance)
#     get_profile.first_name = instance.first_name
#     get_profile.last_name = instance.last_name
#     get_profile.save()
# post_save.connect(update_profile_model, sender=User)

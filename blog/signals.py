from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Blog
   
@receiver(post_save, sender=Blog)
def create_slug(sender, created, instance, **kwargs):
  if created:
    slug_input = f"{instance.title}-{instance.id}"
    instance.slug = slugify(slug_input)
    instance.save()

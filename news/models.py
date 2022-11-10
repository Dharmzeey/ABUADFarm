from django.db import models
from ckeditor.fields import RichTextField


class News(models.Model):
  title = models.CharField(max_length=100)
  body = RichTextField()
  slug = models.SlugField(null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-date_created']
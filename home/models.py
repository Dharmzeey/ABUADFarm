from django.db import models
from ckeditor.fields import RichTextField


class News(models.Model):
  title = models.CharField(max_length=100)
  body = RichTextField()
  date_created = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-date_created']
    

class Blog(models.Model):
  title = models.CharField(max_length=100)
  image = models.ImageField(upload_to="blog")
  body = RichTextField()
  date_created = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-date_created']

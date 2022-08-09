from django.db import models
from django.contrib.auth import settings

from products.models import Product

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_profile"
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=False, blank=False)
    website = models.URLField()
    phone = models.CharField(max_length=11)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.owner)


class Goods(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_goods"
    )
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    add_note = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + " " + str(self.item)
    
    class Meta:
        ordering = ['-date_ordered']


class Messages(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_messages"
    )
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
      return str(self.title) + " message for " + str(self.owner)

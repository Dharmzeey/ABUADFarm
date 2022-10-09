from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import settings

from products.models import UnitName, Product

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    select_sex = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="owner_profile"
    )
    picture = models.ImageField(default="images/avatar.png")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(choices=select_sex, max_length=10)
    phone = models.CharField(max_length=11)
    company_name = models.CharField(max_length=100, null=False, blank=False)
    website = models.URLField()
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.owner)


# THIS MODEL IS FOR EACH GOOD PURCHASED BY CUSTOMERS
class Goods(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_goods"
    )
    unit = models.ForeignKey(UnitName, on_delete=models.CASCADE, related_name="unit_good")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item_good")
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    add_description = models.BooleanField(default=False, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    add_feedback = models.BooleanField(default=True)
    feedback = models.CharField(max_length=225, blank=True, null=True)
    feedback_read = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)
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


class Notification(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_notification"
    )
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name="product_notification")
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
        

class CustomerFeedback(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_feedback"
    )
    product = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name="product_feedback")
    message = models.CharField(max_length=250)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


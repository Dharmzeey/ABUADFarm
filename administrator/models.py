from django.db import models
from django.contrib.auth import settings

from products.models import Product
User = settings.AUTH_USER_MODEL

# Create your models here.

# THIS MODELS ASSIGNS A STAFF(USER) TO A PRODUCT AS THE HEAD WHICH WAS THEN LATER USED IN UNIT CUSTOMER VIEW
class StaffModel(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_staff")
  unit = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="staff_to_unit")
  
  def __str__(self):
    return str(self.owner) + " " + str(self.unit)
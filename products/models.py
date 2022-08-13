from django.db import models


class UnitName(models.Model):
  name = models.CharField(max_length=50)
  
  class Meta:
    ordering = ["name"]
    
  def __str__(self):
    return self.name


class Product(models.Model):
  unit = models.ForeignKey(UnitName, on_delete=models.CASCADE, related_name="unit_product")
  name = models.CharField(max_length=50)

  class Meta:
    ordering = ["unit"]
  
  def __str__(self):
    return self.name

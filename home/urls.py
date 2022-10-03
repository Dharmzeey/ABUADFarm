from django import views
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('units/', views.units, name='units'),
  
  path('farm/agronomy/', views.agronomy, name="agronomy"),
  path('farm/feedmill/', views.feedmill, name="feedmill"),
  path('farm/fishries/', views.fishries, name="fishries"),
  path('farm/honey/', views.honey, name="honey"),
  path('farm/mango-juice/', views.mango_juice, name="mango_juice"),
  path('farm/moringa/', views.moringa, name="moringa"),
  path('farm/piggery/', views.piggery, name="piggery"),
  path('farm/plantain-chips/', views.plantain_chips, name="plantain_chips"),
  path('farm/poultry/', views.poultry, name="poultry"),
  path('farm/wood-factory/', views.wood_factory, name="wood_factory"),
  
]
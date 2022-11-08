from django.contrib import admin
from .models import Profile, Goods, Messages, Country, State, LGA

admin.site.register(Profile)
admin.site.register(Goods)
admin.site.register(Messages)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(LGA)


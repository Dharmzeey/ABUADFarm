from socket import ntohl
from tkinter.messagebox import NO
from django.contrib import admin
from .models import Profile, Goods, Messages, Notification

admin.site.register(Profile)
admin.site.register(Goods)
admin.site.register(Messages)
admin.site.register(Notification)

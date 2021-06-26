from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group

from core.models import CustomUser, Product, Category

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CustomUser)

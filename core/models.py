from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    category_name = models.CharField('Category Name', max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    product_name = models.CharField('Product Name', max_length=100)
    custom_id = models.IntegerField('Custom Product Id', unique=True)
    image_url = models.TextField('Image URL', default='https://picsum.photos/400?image=780')
    is_available = models.BooleanField('Is In Stock', default=True)
    product_price = models.DecimalField('Product Price', max_digits=20, decimal_places=10, default=0.0)
    sell_price = models.DecimalField('Sell Price', max_digits=20, decimal_places=10, default=0.0)
    added_on = models.DateTimeField('Added On', auto_now_add=True)
    last_modified_on = models.DateTimeField('Modified On', auto_now=True)
    product_viewed = models.ManyToManyField('CustomUser', blank=True)
    category = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.product_name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Custom Users"

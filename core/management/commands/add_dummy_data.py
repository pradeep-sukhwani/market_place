import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from core.models import Product, Category, CustomUser
import pandas as pd


class Command(BaseCommand):
    help = 'Adds the dummy data'

    def handle(self, *args, **options):
        with open(os.path.join(os.getcwd(), 'fixtures/users.json')) as users_file_obj:
            user_friends_mapping_dump = json.loads(users_file_obj.read())
        with open(os.path.join(os.getcwd(), 'fixtures/products.json')) as products_file_obj:
            product_detail_dump = json.loads(products_file_obj.read())
        with open(os.path.join(os.getcwd(), 'fixtures/names.json')) as names_file_obj:
            user_detail_dump = json.loads(names_file_obj.read())
        user_friends_data_frame = pd.DataFrame(user_friends_mapping_dump)
        user_detail_data_frame = pd.DataFrame(user_detail_dump)
        user_detail_data_frame = user_detail_data_frame.merge(user_friends_data_frame, on=['id'], how='left')
        user_detail_list = user_detail_data_frame.to_json(orient="records")
        user_detail_list = json.loads(user_detail_list)
        for product_item in product_detail_dump:
            try:
                product_obj = Product.objects.get(custom_id=product_item.get('productId'))
            except Product.DoesNotExist:
                product_obj = Product.objects.create(
                    product_name=product_item.get('productName'),
                    custom_id=product_item.get('productId'),
                    image_url=product_item.get('productImage'),
                    is_available=product_item.get('productStock'),
                    product_price=product_item.get('productPrice'),
                    sell_price=product_item.get('salePrice'),
                )
            self.stdout.write(self.style.SUCCESS(f'Successfully created Product {product_item.get("productName")}'))
            category_obj, category_created = Category.objects.get_or_create(
                category_name=product_item.get('productCategory')
            )
            product_obj.category.add(category_obj)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Category {product_item.get("productCategory")}'))
        for user_item in user_detail_list:
            user, user_created = User.objects.get_or_create(
                email=f'{user_item.get("name").lower().replace(" ", ".")}@testmail.com',
                first_name=user_item.get("name").split(" ")[0],
                last_name=user_item.get("name").split(" ")[1],
                username=user_item.get("name").replace(" ", "."),
            )
            if 'admin' in user_item.get("name").lower():
                user.is_superuser = True
                # user.is_staff = True
            user.set_password('django123')
            user.save()
            if user_created:
                CustomUser.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created User: {user_item.get("name")}'))
        for user_item in user_detail_list:
            user_obj = CustomUser.objects.get(user__email=f'{user_item.get("name").lower().replace(" ", ".")}@testmail.com')
            if user_item.get('following'):
                for user_friends_id in user_item.get('following'):
                    user_obj.friends.add(user_friends_id)
            self.stdout.write(self.style.SUCCESS(f'Successfully added friends for {user_item.get("name")}'))
        self.stdout.write(self.style.SUCCESS('Successfully added all the dummy data in database.'))
        return

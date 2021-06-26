# Market Place Django App
A basic app where a user can create products and based on the user's friends product viewed, you can see the top viewed products and much more.


## Installation
```bash
git clone https://github.com/pssukhwani/market_place.git
cd ~/market_place
pip install -r requirements.txt
```


## Migrate
```bash
python manage.py migrate # Apply Database migration
```

## Load Dummy Data
```bash
python manage.py add_dummy_data # Add dummy data from fixtures
```

## Run Server
```bash
python manage.py runserver # Start Django Server
Home: http://localhost:8000
Admin: http://localhost:8000/market_admin
```

## Login
```
Look at the fixtures > names.json, if the name is Pradeep Sukhwani then
username: pradeep.sukhwani
Default Password for all the users is: django123

To login at Admin: Look for the users that has word 'admin' in it's name, they will be superusers.
```

## API
```
Login:
URL: /api/login
method: POST
data:
  username
  password

Logout:
URL: /api/logout
method: POST

Get all paginated Products:
URL: /api/products/?page=1
method: GET

Add a Product:
URL: /api/products/
method: POST
data:
  product_name
  image_url
  product_price
  sell_price
  category (need ids in list)

Edit Product:
URL: api/products/<product_id>/
method: PATCH
data (fields that can be edited):
  product_name
  image_url
  product_price
  sell_price

Get Product detail:
URL: api/products/<product_id>/
method: GET

Get Top Viewed Products:
URL: api/top_viewed_products/
method: GET
```

from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'core-app'


product_list = views.ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

product_detail = views.ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

login_view = views.LoginView.as_view({
    'post': 'post',
})

logout_view = views.LogoutView.as_view({
    'post': 'post',
})

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('product/<int:id>/', views.DetailView.as_view(), name='product_detail_page'),
]

urlpatterns += format_suffix_patterns([
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/products/', product_list, name='product_list'),
    path('api/products/<int:id>/', product_detail, name='product_detail_api'),
    path('api/top_viewed_products/', views.TopViewedProducts.as_view(), name='top_viewed_products'),
])

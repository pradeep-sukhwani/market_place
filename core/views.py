from copy import deepcopy

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import Product, Category, CustomUser
from core.serializers import ProductSerializer
from django.contrib.auth import authenticate, login, logout


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class DetailView(TemplateView):
    template_name = 'detail.html'

    def get(self, request, *args, **kwargs):
        response = super(DetailView, self).get(request, *args, **kwargs)
        if request.user and request.user.is_authenticated:
            product_obj = Product.objects.get(id=kwargs.get('id'))
            custom_user_obj, created = CustomUser.objects.get_or_create(user=request.user)
            if custom_user_obj not in product_obj.product_viewed.all():
                product_obj.product_viewed.add(custom_user_obj)
        return response


class ProductViewSet(viewsets.ModelViewSet):
    order_by_list = ['-last_modified_on', 'custom_id']
    lookup_url_kwarg = 'id'
    queryset = Product.objects.filter(is_available=True).order_by(*order_by_list)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        category = Category.objects.filter(id__in=request.data.getlist('category'))
        data = deepcopy(request.data)
        data.pop('category')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.category.add(*category)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TopViewedProducts(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_available=True).exclude(product_viewed=None)

    def get_queryset(self):
        query_set = super(TopViewedProducts, self).get_queryset()
        if self.request.user.is_authenticated and self.request.user.friends.all().values_list('id', flat=True):
            query_set = query_set.filter(
                product_viewed__in=list(self.request.user.friends.all().values_list(
                    'id', flat=True)))
        return query_set.order_by('-product_viewed')


class LoginView(viewsets.ViewSet):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        data = {'success': False}
        if user is not None:
            login(request, user)
            data = {'success': True}
            return Response(data)
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class LogoutView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        data = {'success': True}
        return Response(data)

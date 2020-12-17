from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CategoryList, ProductList, ProductDetail, BasketDetail, BasketList, DescriptionProductOrderList, OrderList

app_name = 'api'

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('products/', ProductList.as_view()),
    path('users/<int:pk>', BasketDetail.as_view()),
    path('users/', BasketList.as_view()),
    path('orders/', DescriptionProductOrderList.as_view()),
    path('order/', OrderList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
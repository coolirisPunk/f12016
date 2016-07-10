from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf.urls import patterns, url, include
from rest_framework_nested import routers

router = DefaultRouter()
#router = routers.SimpleRouter()

router.register(r'category_products', CategoryProductViewSet, base_name='category_products')
category_products_router = routers.NestedSimpleRouter(router, r'category_products', lookup='category_product')
category_products_router.register(r'sellers', SellerViewSet, base_name='sellers')
category_products_router.register(r'products', ProductsWithoutCategoryViewSet, base_name='products_without_category')
sellers_router = routers.NestedSimpleRouter(category_products_router, r'sellers', lookup='seller')
sellers_router.register(r'products', ProductViewSet, base_name='products')

urlpatterns = [
        url(r'^', include(router.urls)),
        url(r'^', include(category_products_router.urls)),
        url(r'^', include(sellers_router.urls)),

]


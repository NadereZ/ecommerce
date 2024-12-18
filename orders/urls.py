from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import OrderViewSet
from . import views

router = DefaultRouter()
router.register('', OrderViewSet, basename='orders')

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('', include(router.urls)),
]
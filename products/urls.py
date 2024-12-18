from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from  .views import ProductViewSet

router = DefaultRouter()
router.register('', ProductViewSet, basename='products')

urlpatterns = [
    path('', views.product_list, name='product_list'), # List all products
    path('<int:pk>/', views.product_detail, name='product_detail'), # View product details
    path('search/', views.product_search, name='product_search'), # Search products
    path('', views.home, name='home'), # Route the root URL ('/') to the home view
    path('', include(router.urls)),
    
]

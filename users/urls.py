from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import UserViewSet
from . import views

router = DefaultRouter()
router.register('', UserViewSet, basename='users')


urlpatterns = [
    path('register/',views.register_user, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('', include(router.urls)),
]

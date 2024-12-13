from django.contrib import admin
from .models import CustomUser, Category, Product, Order, OrderItem, Payment, Review
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role'),}),
    )

    admin.site.register(Category)
    admin.site.register(Product)
    admin.site.register(Order)
    admin.site.register(OrderItem)
    admin.site.register(Payment)
    admin.site.register(Review)
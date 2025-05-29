
from django.contrib import admin
from .models import Categories, Products, Clients, Orders, OrderDetail, Cart

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Clients)
admin.site.register(Orders)
admin.site.register(OrderDetail)
admin.site.register(Cart)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # URLs para el carrito
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    # URL para colocar el pedido (Requisito #4)
    path('order/place/', views.place_order, name='place_order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'), # Nueva para confirmación
]
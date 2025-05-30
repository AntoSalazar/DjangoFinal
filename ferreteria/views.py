
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Products, Categories, Cart, Clients, Orders, OrderDetail # Your existing imports
from django.utils import timezone # Your existing import
from django.db.models import F, Sum # Your existing import
from django.db import transaction # <<<<<< ADD THIS LINE

def product_list(request, category_id=None): # category_id ahora es un parámetro opcional
    categories = Categories.objects.all().order_by('name')
    current_category = None # Para saber qué categoría está activa

    if category_id:
        current_category = get_object_or_404(Categories, idcategories=category_id)
        products = Products.objects.filter(idcategories=current_category).order_by('name')
    else:
        products = Products.objects.all().order_by('name')

    
    cart_item_count = 0
    try:
        client = get_current_client(request) 
        if client:
            cart_item_count = Cart.objects.filter(idclient=client).aggregate(total_items=Sum('quantity'))['total_items'] or 0
    except Exception:
        pass

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category, # Pasa la categoría actual a la plantilla
        'cart_item_count': cart_item_count,
    }
    return render(request, 'ferreteria/index.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Products, idproducts=product_id)
    
  
    try:
        client = Clients.objects.get(idclients=1) # Or use request.user if you have custom user model linked to Clients
    except Clients.DoesNotExist:
        # Fallback: Create a dummy client if client 1 doesn't exist.
        # You might want to handle this differently, e.g., redirect to login.
        client = Clients.objects.create(
            idclients=1, 
            name="Default",
            lastname="Client",
            email="default@example.com"
        )
        messages.info(request, "A default client profile was used. Please implement proper client handling.")
    # --- End Client Assumption ---

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = Cart.objects.get_or_create(
            idclient=client,
            idproduct=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f"Updated {product.name} quantity in your cart.")
        else:
            messages.success(request, f"Added {product.name} to your cart.")
        
        return redirect('product_list') # Redirect back to the product list

    
    return redirect('product_list')


def get_current_client(request):
    """
    Función de ayuda para obtener el cliente actual.
    REEMPLAZAR CON LÓGICA DE AUTENTICACIÓN REAL.
    """
    try:
        # Intenta obtener el cliente basado en alguna sesión o usuario autenticado.
        # Por ahora, usaremos el cliente con idclients=1.
        # client_id_from_session = request.session.get('client_id') # Ejemplo si usaras sesiones
        # if client_id_from_session:
        #     return Clients.objects.get(idclients=client_id_from_session)
        return Clients.objects.get(idclients=1)
    except Clients.DoesNotExist:
        messages.error(request, "Client profile not found. Please log in or register. (Using fallback default client)")
        # Fallback: Crear un cliente dummy si no existe el cliente 1 o no hay sesión
        client, _ = Clients.objects.get_or_create(
            idclients=1, # O deja que AutoField maneje esto y luego guárdalo en sesión
            defaults={'name': "Default", 'lastname': "Client", 'email': "default@example.com"}
        )
        # request.session['client_id'] = client.idclients # Guardar en sesión para usos futuros
        return client
# --- Fin Lógica del Cliente ---


def view_cart(request):
    client = get_current_client(request) # Asume que esta función existe y funciona
    cart_items_queryset = Cart.objects.filter(idclient=client).select_related('idproduct')

    # Calcular el conteo total de ítems para la cabecera (suma de cantidades)
    header_cart_item_count = cart_items_queryset.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    # Si prefieres contar productos distintos:
    # header_cart_item_count = cart_items_queryset.count()

    processed_cart_items = []
    total_cart_price = 0
    for item in cart_items_queryset:
        item.total_item_price = item.quantity * item.idproduct.price
        total_cart_price += item.total_item_price
        processed_cart_items.append(item)
        
    context = {
        'cart_items': processed_cart_items,
        'total_cart_price': total_cart_price,
        'cart_item_count': header_cart_item_count, # << AÑADIR ESTO PARA LA CABECERA
    }
    return render(request, 'ferreteria/cart_view.html', context)

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, idcart=item_id)
    client = get_current_client(request)

    if cart_item.idclient != client:
        messages.error(request, "You do not have permission to modify this cart item.")
        return redirect('view_cart')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            if quantity <= cart_item.idproduct.stock:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f"Quantity for {cart_item.idproduct.name} updated.")
            else:
                messages.error(request, f"Not enough stock for {cart_item.idproduct.name}. Available: {cart_item.idproduct.stock}")
        else: # Si la cantidad es 0 o menos, remover el ítem
            cart_item.delete()
            messages.success(request, f"{cart_item.idproduct.name} removed from cart.")
    return redirect('view_cart')

def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, idcart=item_id)
    client = get_current_client(request)

    if cart_item.idclient != client:
        messages.error(request, "You do not have permission to remove this cart item.")
        return redirect('view_cart')
    
    product_name = cart_item.idproduct.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from your cart.")
    return redirect('view_cart')


@transaction.atomic # Ensures all database operations are performed or none at all
def place_order(request):
    if request.method == 'POST':
        client = get_current_client(request)
        cart_items = Cart.objects.filter(idclient=client)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty. Cannot place an order.")
            return redirect('view_cart')

        # Validar stock antes de crear el pedido
        can_place_order = True
        for item in cart_items:
            if item.quantity > item.idproduct.stock:
                messages.error(request, f"Not enough stock for {item.idproduct.name}. Available: {item.idproduct.stock}. Please update your cart.")
                can_place_order = False
        if not can_place_order:
            return redirect('view_cart')

        # Crear el Pedido (Order)
        new_order = Orders.objects.create(
            idclients=client,
            order_date=timezone.now().date(),
            state='pendiente' # Estatus inicial
        )

        # Crear los Detalles del Pedido (OrderDetail) y actualizar stock
        for item in cart_items:
            OrderDetail.objects.create(
                idorders=new_order,
                idproducts=item.idproduct,
                quantity=item.quantity,
                unit_price=item.idproduct.price # Precio al momento de la compra
            )
            # Decrementar el stock del producto
            product_to_update = item.idproduct
            product_to_update.stock = F('stock') - item.quantity # F() para evitar race conditions
            product_to_update.save()
        
        # Vaciar el carrito del cliente
        cart_items.delete()

        messages.success(request, f"Order #{new_order.idorders} has been placed successfully! It belongs to client {new_order.idclients.name}.")
        return redirect('order_confirmation', order_id=new_order.idorders)

    # Si no es POST, redirigir al carrito
    return redirect('view_cart')

def order_confirmation(request, order_id):
    order = get_object_or_404(Orders, idorders=order_id)
    client = get_current_client(request) # Asume que esta función existe y funciona

    # Verificar que el cliente viendo la confirmación sea el dueño del pedido
    if order.idclients != client:
        messages.error(request, "You are not authorized to view this order confirmation.")
        return redirect('product_list') # O a donde consideres apropiado
        
    order_details_queryset = OrderDetail.objects.filter(idorders=order).select_related('idproducts')
    
    processed_order_details = []
    total_order_price = 0
    for detail in order_details_queryset:
        detail.total_item_price = detail.quantity * detail.unit_price # Calcula el total por ítem
        total_order_price += detail.total_item_price
        processed_order_details.append(detail)

    # Obtener el conteo actual de ítems en el carrito (para la cabecera)
    # Este sería un nuevo carrito o ítems que quedaron/se añadieron después de este pedido.
    header_cart_item_count = 0
    if client: # Solo si tenemos un cliente
        header_cart_item_count = Cart.objects.filter(idclient=client).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    context = {
        'order': order,
        'order_details': processed_order_details,
        'total_order_price': total_order_price,
        'cart_item_count': header_cart_item_count, # << AÑADIR ESTO PARA LA CABECERA
    }
    return render(request, 'ferreteria/order_confirmation.html', context)


def product_detail_view(request, product_id):
    product = get_object_or_404(Products.objects.select_related('idcategories'), idproducts=product_id) #
    categories = Categories.objects.all().order_by('name') # Para el sidebar, si decides incluirlo

    # Lógica para el contador del carrito (similar a product_list)
    cart_item_count = 0
    try:
        client = get_current_client(request) #
        if client:
            cart_item_count = Cart.objects.filter(idclient=client).aggregate(total_items=Sum('quantity'))['total_items'] or 0
    except Exception:
        pass # Mantener cart_item_count en 0 si hay error o no hay cliente

    context = {
        'product': product,
        'categories': categories, # Opcional, si quieres mostrar el sidebar de categorías
        'cart_item_count': cart_item_count,
        # Puedes añadir 'current_category': product.idcategories para resaltar en el sidebar si lo usas
    }
    return render(request, 'ferreteria/product_detail.html', context)

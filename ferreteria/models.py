
from django.db import models
from django.utils import timezone

class Categories(models.Model):
    idcategories = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    image = models.ImageField(upload_to='categories_images/', null=True, blank=True, verbose_name="Image") 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category" 
        verbose_name_plural = "Categories"

class Products(models.Model):
    idproducts = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255, null=True, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    idcategories = models.ForeignKey(Categories, on_delete=models.PROTECT, db_column='idcategories', null=True, blank=True, verbose_name="Category") 
    image = models.ImageField(upload_to='products_images/', null=True, blank=True, verbose_name="Image") 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product" 
        verbose_name_plural = "Products" 

class Clients(models.Model):
    idclients = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True, verbose_name="Name") 
    lastname = models.CharField(max_length=45, null=True, blank=True, verbose_name="Last Name") 
    email = models.EmailField(max_length=45, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=45, null=True, blank=True, verbose_name="Phone") 

    def __str__(self):
        if self.name and self.lastname:
            return f"{self.name} {self.lastname}"
        elif self.name:
            return self.name
        elif self.email:
            return self.email
        return f"Client ID: {self.idclients}"

    class Meta:
        verbose_name = "Client" 
        verbose_name_plural = "Clients" 

class Orders(models.Model):
    idorders = models.AutoField(primary_key=True)
    idclients = models.ForeignKey(Clients, on_delete=models.PROTECT, db_column='idclients', null=True, blank=True, verbose_name="Client") 
    order_date = models.DateField(null=True, blank=True, verbose_name="Order Date") 
    state = models.CharField(max_length=45, null=True, blank=True, default='pending', verbose_name="State") 

    def __str__(self):
        client_obj = self.idclients
        client_str = str(client_obj) if client_obj else "N/A"
        return f"Order #{self.idorders} - Client: {client_str}"

    class Meta:
        verbose_name = "Order" 
        verbose_name_plural = "Orders"

class OrderDetail(models.Model):
    idorder_detail = models.AutoField(primary_key=True)
    idorders = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='idorders', null=True, blank=True, verbose_name="Order")
    idproducts = models.ForeignKey(Products, on_delete=models.PROTECT, db_column='idproducts', null=True, blank=True, verbose_name="Product") 
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Quantity") 
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Unit Price")

    def __str__(self):
        order_id_str = self.idorders.idorders if self.idorders else "N/A"
        product_obj = self.idproducts
        product_str = str(product_obj) if product_obj else "N/A"
        return f"Detail for Order #{order_id_str} - Product: {product_str}"

    class Meta:
        verbose_name = "Order Detail" 
        verbose_name_plural = "Order Details"

class Cart(models.Model):
    idcart = models.AutoField(primary_key=True)
    idclient = models.ForeignKey(Clients, on_delete=models.CASCADE, db_column='idclient', verbose_name="Client")
    idproduct = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='idproduct', verbose_name="Product")
    quantity = models.IntegerField(verbose_name="Quantity") 
    added_date = models.DateTimeField(default=timezone.now, verbose_name="Added Date") 

    def __str__(self):
        client_obj = self.idclient
        product_obj = self.idproduct
        client_str = str(client_obj) if client_obj else "N/A"
        product_str = str(product_obj) if product_obj else "N/A"
        return f"Cart item for Client {client_str} - Product: {product_str}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = [['idclient', 'idproduct']]
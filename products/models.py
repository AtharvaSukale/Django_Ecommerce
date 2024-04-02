from django.db import models
from django.utils import timezone
from products.storage import OverriteFile


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)
    
def get_image_filepath(self, filename):
    return f'./products/{self.name}_{self.created_date_time}.png'

def get_default_image():
    return f'./products/default.png'  

class Product(models.Model):
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE, related_name='product_category', blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to=get_image_filepath, default=get_default_image, storage=OverriteFile(), blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=True)
    price = models.FloatField(max_length=64, blank=False, null=False)
    is_recommended = models.BooleanField(default=True)
    created_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
    
class Order(models.Model):
    
    DELIVERY_METHODS = [
        ((1, 'Courier delivery')),
        ((2, 'Pickup at a parcel locker')),
        ((3, 'Personal pickup')),     
    ]
    
    PAYMENT_METHODS = [
        ((1, 'Cash/card payment on delivery')),
        ((2, 'Online payment by credit card')),
        ((3, 'Cash on Delivery')),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='order_user', blank=True, null=True)
    first_name_order = models.CharField(max_length=255, blank=False, null=False)
    last_name_order = models.CharField(max_length=255, blank=False, null=False)
    delivery_method_order = models.IntegerField(choices=DELIVERY_METHODS, default=1, blank=False, null=False)
    payment_method_order = models.IntegerField(choices=PAYMENT_METHODS, default=1, blank=False, null=False)
    country_order = models.CharField(max_length=255, blank=False, null=False)
    city_order = models.CharField(max_length=255, blank=False, null=False)
    street_order = models.CharField(max_length=255, blank=False, null=False)
    house_number_order = models.CharField(max_length=255, blank=False, null=False)
    zip_code_order = models.CharField(max_length=255, blank=False, null=False)
    phone_number_order = models.CharField(max_length=255, blank=False, null=False)
    email_order = models.EmailField(max_length=255, blank=False, null=False)
    date_time_order = models.DateTimeField(default=timezone.now, blank=False, null=False)
     
    def __str__(self):
        return str(self.id) 

class OrderProduct(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='orderproduct_product', blank=False, null=False)
    quantity = models.FloatField(default=1.0, blank=False, null=False)
    order_id = models.ForeignKey("products.Order", on_delete=models.CASCADE, related_name='orderproduct_order_id', blank=True, null=True)

    # @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.id)
    
class Opinion(models.Model):
    product =  models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='opinion_product', blank=False, null=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='opinion_user', blank=False, null=False)
    rating = models.CharField(max_length=1, blank=False, null=False, default='5')
    content = models.CharField(max_length=1024, blank=True, null=True)
    created_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        unique_together = ('product', 'user')


    def __str__(self):
        return str(self.id)
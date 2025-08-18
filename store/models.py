from django.db import models

# Create your models here.
class Customer(models.Model):
    MEMBERSHIP_BASIC = 'Basic'
    MEMBERSHIP_BRONZE = 'Bronze'
    MEMBERSHIP_SILVER = 'Silver'
    MEMBERSHIP_GOLD = 'Gold'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BASIC, 'Basic'),
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BASIC)
    
    class Meta:
        db_table = 'store_customer'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete= models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"{self.customer}; City: {self.city}, Street: {self.street}"
   
    
class Promotion(models.Model):
    description = models.TextField()
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    slug = models.SlugField(default="-")
    title = models.CharField(max_length=255 )
    description = models.TextField()
    unit_price = models.DecimalField(max_digits= 10, decimal_places= 2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    
    def __str__(self):
        return self.title
    

    
class Order(models.Model):
    PENDING = 'Pending'
    COMPLETE = 'Complete'
    FAILED = 'Failed'
    
    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (FAILED, 'Failed'),
           
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS)
    
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    
    def __str__(self):
        return f"Order by {self.customer} placed on {self.placed_at}. Payment status: {self.payment_status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"Product: {self.product}, Qauntity: {self.quantity}"


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    



    


    


    
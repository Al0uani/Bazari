from django.db import models


class user(models.Model):
    Username = models.CharField(unique=True,max_length=10)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Birth = models.DateField()
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=64)
    Pfp = models.ImageField(upload_to='user/')
    
    def __str__(self):
        return f"ID:{self.pk}-{self.Username}"

class product(models.Model):
    Name = models.CharField(max_length=50)
    Description = models.TextField(max_length=250)
    Owner = models.ForeignKey(user, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Picture_main = models.ImageField(upload_to='product/')
    Picture_second = models.ImageField(upload_to='product/', blank=True, null=True)
    Picture_third = models.ImageField(upload_to='product/', blank=True, null=True) 
    CATEGORY_CHOICES = [
    ('art', 'Art'),
    ('deco', 'Deco'),
    ('clothing', 'Clothing'),
    ('antiques', 'Antiques'),]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=None,null=True)

    def __str__(self):
        return self.Name

class ContactUs(models.Model): 
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=200)

    def __str__(self):
        return f"ContactUs(id={self.id}, name={self.name},email={self.email},phone={self.phone},msg={self.message})"
    


class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)  # One cart per user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):

        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.Price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.Name}"

class HistoryPayment(models.Model):
    User = models.ForeignKey(user, on_delete=models.CASCADE)
    Item = models.ForeignKey(product,on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.User}"

from django.contrib import admin
from .models import user,product,ContactUs,Cart,CartItem,HistoryPayment


class HistoryPaymentAdmin(admin.ModelAdmin):
    list_display = ('User', 'Item', 'payment_method', 'date')  
    list_filter = ('payment_method', 'date')  
    search_fields = ('User__username', 'Item__name') 

class ProductAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Owner', 'Price', 'category')  
    list_filter = ('Price', 'category','Owner') 

class UsersAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Email', 'Password')  

class ContactAdmin(admin.ModelAdmin): 
    list_display = ('name', 'email','message') 

admin.site.register(product,ProductAdmin)
admin.site.register(HistoryPayment, HistoryPaymentAdmin)
admin.site.register(user,UsersAdmin)
admin.site.register(ContactUs,ContactAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
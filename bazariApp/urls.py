from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.homepage, name='home'),
    path('SignUp/',views.SignUp,name='signup'),
    path('LogIn/',views.login, name='login'),
    path('LogOut/',views.logout,name='logout'),
    path('AddProduct/',views.add_product, name='addproduct'),
    path('Contact-Us/',views.contactus, name="contactus"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('Products/',views.products,name='products'),
    path('Checkout/',views.checkout,name="checkout"),
    path('Metamask/',views.metamask,name="metamask"),
    path('Process/',views.Process,name="process"),
    path('Invoice/',views.invoice,name="invoice"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
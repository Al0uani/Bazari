from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpFrom,ProductForm
from .models import user,product,ContactUs,Cart,CartItem,HistoryPayment
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime


def sessions_nav(request):
    username = request.session.get('username') 
    if username:
        user_instance = user.objects.get(Username=username)  
        pfp = user_instance.Pfp.url 
        cart, created = Cart.objects.get_or_create(user=user_instance)
    else:
        pfp = None
        cart = None

    try:
        access_token = request.session.get('access_token', None)

        if access_token:
            
            AccessToken(access_token)  
            request.session['status_log'] = True 
        else:
            request.session['status_log'] = False  

    except TokenError:
        refresh_token = request.session.get('refresh_token', None)
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                # Generate a new access token
                new_access_token = str(refresh.access_token)
                request.session['access_token'] = new_access_token
                request.session['status_log'] = True 
            except TokenError:
                
                request.session['status_log'] = False
        else:
            request.session['status_log'] = False  

    
    context = {
        'status_log': request.session.get('status_log', False),
        'payment':request.session.get('payment', None),
        'username': username,
        'pfp': pfp,
        'cart': cart,
        'category': product.CATEGORY_CHOICES,
    }
    return context


def homepage(request):
    context = sessions_nav(request)
    products = product.objects.all()
    context['products'] = products
    return render(request, 'pages/main.html', context)


def SignUp(request):
    if request.session.get('status_log') == True:
        return redirect('home') 
    if request.method == 'POST':
        form = SignUpFrom(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user_instance = user.objects.get(Username=form.cleaned_data.get('Username'))
            refresh = RefreshToken.for_user(user_instance)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            request.session['user_id'] = user_instance.pk
            request.session['username'] = form.cleaned_data.get('Username')
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token 
            messages.success(request, "Sign up successful!")  
            return redirect('home')
    else:
        form = SignUpFrom()
    return render(request, 'pages/Signup_form.html', {'form': form})

def login(request):
    if request.session.get('status_log') == True:
        return redirect('home') 
    if request.method == 'POST':
        request.session.flush()  
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_instance = user.objects.get(Email=email)
            if user_instance.Password == password:
                request.session['user_id'] = user_instance.pk
                request.session['username'] = user_instance.Username
                refresh = RefreshToken.for_user(user_instance)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token 
                return redirect('home')  
            else:
                messages.error(request, 'Invalid password.')
        except user.DoesNotExist:
            messages.error(request, 'No user found with this email.')

    return render(request, 'pages/signin_form.html')

def logout(request):
    request.session.flush()  
    return redirect('home')  

def add_product(request):
    context = sessions_nav(request)  

    if context['status_log'] == False:
        return redirect('home')  
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.Owner = user.objects.get(Username=context['username'])  
            product.save()
            return redirect('home')  
    else:
        form = ProductForm()  

    context['form'] = form
    return render(request, 'pages/add_product.html', context)

def contactus(request):
    context = {
        'contact_sent': request.session.get('contact_sent', False),
    }

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('home')
        elif 'submit' in request.POST:
            # Retrieve form data
            name = request.POST.get('Name')
            phone = request.POST.get('Phone')
            email = request.POST.get('Email')
            msg = request.POST.get('Message')
            
            # Save contact message
            ContactUs.objects.create(name=name, phone=phone, email=email, message=msg)
            
            # Set the session flag
            request.session['contact_sent'] = True
            
            #
            return redirect('contactus')

    
    if context['contact_sent']:
        request.session['contact_sent'] = False

    return render(request, 'pages/contact-us.html', context)



def add_to_cart(request, product_id):
    username = request.session.get('username') 
    user_instance = user.objects.get(Username=username)  
    Product = get_object_or_404(product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=user_instance)
    cart_item,created = CartItem.objects.get_or_create(cart=cart, product=Product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('home')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        username = request.session.get('username') 
        user_instance = user.objects.get(Username=username)  
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user_instance)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('home')

def products(request):
    context = sessions_nav(request)
    products = product.objects.all()
    context['products'] = products
    return render(request,'pages/products_list.html',context)

def checkout(request):
    context = sessions_nav(request)
    if request.method == 'POST':
        if 'subbtn' in request.POST:
            choice = request.POST.get('payment')
            if(choice == 'metamask'):
                request.session['payment']="Metamask"
                return render(request,'pages/metamask.html',context)
            else:
                return redirect('home')

    return render(request,'pages/checkout.html',context)

def metamask(request):
    context = sessions_nav(request)
    return render(request,'pages/metamask.html',context)

def test(request):
    context = sessions_nav(request)
    return render(request,'pages/test.html',context)

def Process(request):
    context = sessions_nav(request)
    user_instance = user.objects.get(Username=context['username'])
    cart_item = CartItem.objects.filter(cart__user=user_instance)
    for i in cart_item:
        HistoryPayment.objects.create(
            User = user_instance,
            Item = i.product,
            Quantity= i.quantity,
            payment_method = context['payment'],
            date = datetime.now(),
        )


    cart_item.delete()
    return redirect('home')
    
    
def invoice(request):
    context = sessions_nav(request)
    return render(request,'store/invoice.html' , context)
from django.shortcuts import render,redirect
from . models import Cart, Customer, Product,OrderPlaced,Wishlist
from django.views import View
from django.http import JsonResponse
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
import paypalrestsdk
from django.conf import settings
# views.py
from django.db.models import Q

# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user=request.user))
        product =Product.objects.filter(category=val)
        title =Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product =Product.objects.filter(category=val)
        title =Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        product =Product.objects.filter(category=val)
        return render(request,"app/category.html",locals())


@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            user = request.user
            totalitem = Cart.objects.filter(user=user).count()
            wishitem = Wishlist.objects.filter(user=user).count()
            wishlist = Wishlist.objects.filter(user=user, product=product)
        else:
            wishlist = None

        context = {
            'product': product,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'wishlist': wishlist,
        }

        return render(request, "app/productdetail.html", context)


       

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/customerregistration.html",locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
            return redirect('login')  # Redirect to the login page or another relevant page
        else:
            messages.warning(request, "Invalid input data")
            return render(request, "app/customerregistration.html", {'form': form})
     

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            division = form.cleaned_data['division']
            zipcode = form.cleaned_data['zipcode']
            
            # Save the customer profile
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, division=division, zipcode=zipcode)
            reg.save()
            
            messages.success(request, "Congratulations! Profile saved successfully.")
            # Redirect to avoid resubmission on refresh
            return redirect('profile')
        
        else:
            messages.warning(request, "Invalid input data.")
        
        # Render the form again in case of invalid input
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

        

def address(request):        
    add =Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
       form = CustomerProfileForm(request.POST)
        
       if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name =form.changed_data['name']
            add.locality =form.cleaned_data['locality']
            add.city =form.cleaned_data['city']
            add.mobile =form.cleaned_data['mobile']
            add.state =form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()  
            messages.success(request, "Congratulations! Profile updated successfully.")
          
            
       else:
            messages.warning(request, "Invalid input data.")
            return redirect("address")
        


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    print(f"User: {user}")
    print(f"Authenticated: {user.is_authenticated}")
    print(f"Session Key: {request.session.session_key}")
    print(f"Session Data: {dict(request.session.items())}")
    print(f"User {user} is trying to add product {product_id} to the cart.")
    
    if product_id is None:
        print("No product_id provided in GET request.")
        return redirect("/")

    try:
        # Ensure product_id is clean and an integer
        product_id = product_id.strip().rstrip('/')  # Remove leading/trailing whitespace and slashes
        product_id = int(product_id)  # Convert to integer
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("/cart")
    except ValueError:
        print(f"Invalid product_id: {product_id}.")
        return redirect("/")
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} does not exist.")
        return redirect("/")
    except Exception as e:
        print(f"Error adding product {product_id} to cart for user {user}: {e}")
        return redirect("/")

@login_required
def show_cart(request):
    user=request.user
    cart =Cart.objects.filter(user=user)
    amount =0
    for p in cart:
        value =p.quantity * p.product.discounted_price
        amount =amount +value
    totalamount =amount +40  
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
     wishitem = len(Wishlist.objects.filter(user=request.user)) 
    return render(request,'app/addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40
        return render(request, 'app/checkout.html', locals())

    def post(self, request):
        user = request.user
        address_id = request.POST.get('address') 
        cart_items = Cart.objects.filter(user=user)

        if not address_id:
            messages.error(request, "Please select an address.")
            return redirect('checkout')  

        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('home')  
    
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@login_required
def create_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency = 'Tk.' 
        
        # Create PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": currency
                },
                "description": "Order payment"
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/success/'),
                "cancel_url": request.build_absolute_uri('/payment/cancel/')
            }
        })
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            return JsonResponse({'error': 'Payment creation failed'}, status=400)

@login_required
def payment_execution(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html')

@login_required    
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/orders.html',locals())

@login_required    
def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        user =request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart :
            value =p.quantity *p.product.discounted_price
            amount =amount +value
            totalamount =amount +40

        print(prod_id)
        data={
               'quantity':c.quantity,
               'amount': amount,
               'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required 
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        user =request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart :
            value =p.quantity *p.product.discounted_price
            amount =amount +value
            totalamount =amount +40

        print(prod_id)
        data={
               'quantity':c.quantity,
               'amount': amount,
               'totalamount':totalamount
        }
        return JsonResponse(data)   
    


@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
            c.delete()
            
            # Recalculate the cart totals
            cart = Cart.objects.filter(user=user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart)
            totalamount = amount + 40

            data = {
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)


@login_required
def wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    context = {
        'wishlist_items': wishlist_items,
    }
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/wishlist.html', locals())

@login_required        
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Addded Successfully',
        }
        return JsonResponse(data)


from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Wishlist, Product

@login_required
def minus_wishlist(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()
            return redirect('wishlist')  # Redirect to the wishlist page after removing the item
        else:
            data = {
                'message': 'Item not found in Wishlist',
            }
            return JsonResponse(data)

@login_required    
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      wishitem = len(Wishlist.objects.filter(user=request.user)) 
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())



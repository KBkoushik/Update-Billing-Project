from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from .models import UserDetails, AddProduct, BillDetails, InvoiceProductDetails

# Create your views here.
def hompageView(request):
    return render(request,'bapp/homepage.html')


def invoice_view(request):
    return render(request,'bapp/invoice.html')


def sign_in_page_view(request):

    return render(request, 'bapp/signin.html')  # Render your homepage or a different template

    

from django.shortcuts import render, redirect
from .models import UserDetails

def sign_in_view(request, m_no=None):
    if request.method == 'POST' or m_no:
        if not m_no:
            m_no = request.POST.get('email')  # assuming 'email' is the name of the input field in your form
        
        if m_no:
            try:
                user = UserDetails.objects.get(mob_no=m_no)
                user_name = user.user_name
                sign_in_dict = {
                    'name': user_name.upper(),
                    'mobile_no': m_no,
                }
                return render(request, 'bapp/userdashboard.html', sign_in_dict)
            except UserDetails.DoesNotExist:
                return redirect('user_address')
    return render(request, 'bapp/signin.html')

def input_user_details_view(request):
    if request.method == 'POST':
        new_user_name = request.POST.get('user_name')
        new_company_name = request.POST.get('company_name')
        new_company_address = request.POST.get('company_address')
        new_pincode = request.POST.get('pincode')
        m_no = request.POST.get('mob_no')  # Assuming you collect this from the form as well

        if new_user_name and new_company_name and new_company_address and new_pincode and m_no:
            new_user = UserDetails(
                mob_no=m_no,
                user_name=new_user_name,
                user_company_name=new_company_name,
                user_company_address=new_company_address,
                user_company_pincode=new_pincode
            )
            new_user.save()
            return redirect('sign_in')  # Redirect to a URL pattern named 'user_address'
    return render(request, 'bapp/user_details.html')   



def add_product_view(request, string1):
    user = None
    if request.method == 'POST':
        name = request.POST.get('name')
        details = request.POST.get('details')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        selling_price = request.POST.get('selling_price')
        action = request.POST.get('action')

        try:
            user = UserDetails.objects.get(mob_no=string1)
        except UserDetails.DoesNotExist:
            user = None

        if user:
            if AddProduct.objects.filter(user=user, name=name).exists():
                # Product already exists
                message = f"Product '{name}' already exists for this user."
                return render(request, 'bapp/add_product.html', {'message': message, 'user': user})

            new_product = AddProduct(
                user=user,
                name=name,
                details=details,
                quantity=quantity,
                price=price,
                selling_price=selling_price
            )
            new_product.save()
            if action == 'add_more':
                return render(request, 'bapp/add_product.html', {'message': 'Product added successfully!', 'user': user})
            elif action == 'save':
                return redirect('sign_in')  # Redirect to a welcome page
    return render(request, 'bapp/add_product.html', {'user': user})

def generate_invoice_view(request, mob_no):
    try:
        user = UserDetails.objects.get(mob_no=mob_no)
    except UserDetails.DoesNotExist:
        return redirect('user_address')  # redirect if user does not exist

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_mobile_no = request.POST.get('customer_mobile_no')
        customer_address = request.POST.get('customer_address')

        # Generate bill number
        last_bill = BillDetails.objects.filter(user=user).order_by('bill_number').last()
        if last_bill:
            new_bill_number = str(int(last_bill.bill_number) + 1).zfill(6)
        else:
            new_bill_number = '000001'

        # Get current date and time
        current_date = timezone.now().date()
        current_time = timezone.now().time().replace(second=0, microsecond=0)

        # Initialize bill amount
        bill_amount = 0

        # Collect product details from the form
        products = []
        for i in range(len(request.POST.getlist('product_name'))):
            product_name = request.POST.getlist('product_name')[i]
            product_quantity = int(request.POST.getlist('product_quantity')[i])
            product = AddProduct.objects.get(user=user, name=product_name)
            total_product_amount = product.selling_price * product_quantity
            bill_amount += total_product_amount

            products.append({
                'product_name': product_name,
                'product_description': product.details,
                'product_quantity': product_quantity,
                'total_amount': total_product_amount
            })

            # Update the quantity in AddProduct model
            product.quantity -= product_quantity
            product.save()

        # Save BillDetails
        bill = BillDetails.objects.create(
            user=user,
            bill_number=new_bill_number,
            bill_date=current_date,
            bill_time=current_time,
            customer_name=customer_name,
            customer_mobile_no=customer_mobile_no,
            customer_address=customer_address,
            bill_amount=bill_amount
        )

        # Save InvoiceProductDetails
        for product in products:
            InvoiceProductDetails.objects.create(
                bill_number=bill,
                user=user,
                date=current_date,
                product_name=product['product_name'],
                product_description=product['product_description'],
                product_quantity=product['product_quantity'],
                total_amount=product['total_amount']
            )

        return redirect('process_email', m_no=mob_no)

    products = AddProduct.objects.filter(user=user)
    context = {
        'user': user,
        'products': products,
    }
    return render(request, 'bapp/generate_invoice.html', context)

def customer_details_view(request, mob_no):
    user = get_object_or_404(UserDetails, mob_no=mob_no)
    
    # Fetching first 10 customer details
    customer_details_list = BillDetails.objects.filter(user=user)[:10]
    
    paginator = Paginator(customer_details_list, 5)  # 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customer_details': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
        'mob_no': mob_no,
    }
    return render(request, 'bapp/customer_details.html', context)

def transaction_details_view(request, mob_no):
    user = get_object_or_404(UserDetails, mob_no=mob_no)
    
    # Fetching first 5 transaction details
    transaction_list = InvoiceProductDetails.objects.filter(user=user).order_by('-date')[:5]
    
    paginator = Paginator(transaction_list, 5)  # 5 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'transactions': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
        'mob_no': mob_no,
    }
    return render(request, 'bapp/transaction_details.html', context)

def help_view(request):
    return render(request, 'bapp/help.html')    
            



import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot_view(request):
    # Generate some sample data
    x = ['A', 'B', 'C', 'D', 'E']
    y = [10, 20, 15, 25, 30]

    # Create bar plot
    plt.bar(x, y)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Plot')

    # Convert plot to image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_str = "data:image/png;base64," + base64.b64encode(image_png).decode()

    plt.close()  # Close plot to free memory

    return render(request, 'bapp/plot.html', {'image': image_str})
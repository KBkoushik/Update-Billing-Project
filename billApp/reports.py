import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils import timezone
from datetime import timedelta
import pytz
from django.shortcuts import render
from django.db.models import Sum
from .models import BillDetails, InvoiceProductDetails, AddProduct

def get_plot():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def generate_report_plots(user_id):
    plt.switch_backend('AGG')

    tz = pytz.timezone('Asia/Kolkata')
    today = timezone.now().astimezone(tz)
    current_month = today.month
    current_year = today.year

    # Top 5 Days with Lowest Sales (This Month)
    bills = BillDetails.objects.filter(user_id=user_id, bill_date__month=current_month, bill_date__year=current_year)
    daily_sales = bills.values('bill_date').annotate(total_amount=Sum('bill_amount')).order_by('total_amount')[:5]

    dates = [sale['bill_date'] for sale in daily_sales]
    amounts = [sale['total_amount'] for sale in daily_sales]

    plt.figure()
    plt.bar(dates, amounts, color='red')
    plt.xlabel('Date')
    plt.xticks(rotation=90)
    plt.ylabel('Sales Amount')
    plt.title('Top 5 Days with Lowest Sales (This Month)')
    lowest_sales_days_plot = get_plot()
    plt.close()

    # Top 5 Unsold High-Quantity Products
    sold_products = InvoiceProductDetails.objects.filter(user_id=user_id).values_list('product_name', flat=True).distinct()
    unsold_products = AddProduct.objects.filter(user_id=user_id).exclude(name__in=sold_products).order_by('-quantity')[:5]

    product_names = [product.name for product in unsold_products]
    quantities = [product.quantity for product in unsold_products]

    plt.figure()
    plt.bar(product_names, quantities, color='blue')
    plt.xlabel('Product Name')
    plt.xticks(rotation=90)
    plt.ylabel('Quantity')
    plt.title('Top 5 Unsold High-Quantity Products')
    unsold_products_plot = get_plot()
    plt.close()

    # Top 5 Products with Low Stock
    low_stock_products = AddProduct.objects.filter(user_id=user_id).order_by('quantity')[:5]

    product_names = [product.name for product in low_stock_products]
    quantities = [product.quantity for product in low_stock_products]

    plt.figure()
    plt.bar(product_names, quantities, color='purple')
    plt.xlabel('Product Name')
    plt.xticks(rotation=90)
    plt.ylabel('Quantity')
    plt.title('Top 5 Products with Low Stock')
    low_stock_products_plot = get_plot()
    plt.close()

    # Top 5 Selling Products (Last Month)
    last_month = (today - timedelta(days=30)).month
    top_selling_products = InvoiceProductDetails.objects.filter(user_id=user_id, date__month=last_month).values('product_name').annotate(total_quantity=Sum('product_quantity')).order_by('-total_quantity')[:5]

    product_names = [product['product_name'] for product in top_selling_products]
    quantities = [product['total_quantity'] for product in top_selling_products]

    plt.figure()
    plt.bar(product_names, quantities, color='green')
    plt.xlabel('Product Name')
    plt.xticks(rotation=90)
    plt.ylabel('Quantity Sold')
    plt.title('Top 5 Selling Products (Last Month)')
    top_selling_products_plot = get_plot()
    plt.close()

    # Daily Revenue (Last 5 Days)
    daily_revenue = bills.values('bill_date').annotate(
        total_revenue=Sum('bill_amount')
    ).order_by('-bill_date')[:5]

    dates = [rev['bill_date'] for rev in daily_revenue]
    revenues = [rev['total_revenue'] for rev in daily_revenue]

    plt.figure()
    plt.bar(dates, revenues, color='orange')
    plt.xlabel('Date')
    plt.xticks(rotation=90)
    plt.ylabel('Revenue')
    plt.title('Daily Revenue (Last 5 Days)')
    daily_revenue_plot = get_plot()
    plt.close()

    # Monthly Revenue (Last 5 Months)
    monthly_revenue = bills.values('bill_date__year', 'bill_date__month').annotate(
        total_revenue=Sum('bill_amount')
    ).order_by('-bill_date__year', '-bill_date__month')[:5]

    months = [f"{rev['bill_date__month']}-{rev['bill_date__year']}" for rev in monthly_revenue]
    revenues = [rev['total_revenue'] for rev in monthly_revenue]

    plt.figure()
    plt.bar(months, revenues, color='brown')
    plt.xlabel('Month')
    plt.xticks(rotation=90)
    plt.ylabel('Revenue')
    plt.title('Monthly Revenue (Last 5 Months)')
    monthly_revenue_plot = get_plot()
    plt.close()

    # Yearly Revenue (Last 5 Years)
    yearly_revenue = bills.values('bill_date__year').annotate(
        total_revenue=Sum('bill_amount')
    ).order_by('-bill_date__year')[:5]

    years = [rev['bill_date__year'] for rev in yearly_revenue]
    revenues = [rev['total_revenue'] for rev in yearly_revenue]

    plt.figure()
    plt.bar(years, revenues, color='cyan')
    plt.xlabel('Year')
    plt.xticks(rotation=90)
    plt.ylabel('Revenue')
    plt.title('Yearly Revenue (Last 5 Years)')
    yearly_revenue_plot = get_plot()
    plt.close()

    return {
        'lowest_sales_days_plot': lowest_sales_days_plot,
        'unsold_products_plot': unsold_products_plot,
        'low_stock_products_plot': low_stock_products_plot,
        'top_selling_products_plot': top_selling_products_plot,
        'daily_revenue_plot': daily_revenue_plot,
        'monthly_revenue_plot': monthly_revenue_plot,
        'yearly_revenue_plot': yearly_revenue_plot,
    }

def reports_view(request, user_id):
    plots = generate_report_plots(user_id)
    return render(request, 'bapp/reports.html', plots)

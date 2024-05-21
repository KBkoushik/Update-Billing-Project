from django.contrib import admin
from billApp.models import *

# Register your models here.
class UserDetailsAdmin(admin.ModelAdmin):
        list_display = ('mob_no', 'user_name', 'user_company_name', 'user_company_address', 'user_company_pincode')
admin.site.register(UserDetails,UserDetailsAdmin)

class ProducDetailsAdmin(admin.ModelAdmin):
        list_display = ('user', 'name', 'details', 'quantity', 'price', 'selling_price')
admin.site.register(AddProduct,ProducDetailsAdmin)

@admin.register(BillDetails)
class BillDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bill_number', 'bill_date', 'bill_time', 'customer_name', 'customer_mobile_no', 'customer_address', 'bill_amount')

@admin.register(InvoiceProductDetails)
class InvoiceProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('user','bill_number', 'date', 'product_name', 'product_description', 'product_quantity', 'total_amount')


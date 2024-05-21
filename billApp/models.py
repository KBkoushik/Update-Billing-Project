from django.db import models

# Create your models here.
class UserDetails(models.Model):
    mob_no = models.CharField(primary_key=True, max_length=13)
    user_name = models.CharField(max_length=20)
    user_company_name = models.CharField(max_length=50)
    user_company_address = models.CharField(max_length=70)
    user_company_pincode = models.BigIntegerField()

class AddProduct(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    details = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

class BillDetails(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=6)
    bill_date = models.DateField()
    bill_time = models.TimeField()
    customer_name = models.CharField(max_length=100)
    customer_mobile_no = models.CharField(max_length=15)
    customer_address = models.CharField(max_length=200)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)

class InvoiceProductDetails(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    bill_number = models.ForeignKey(BillDetails, on_delete=models.CASCADE)
    date = models.DateField()
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    



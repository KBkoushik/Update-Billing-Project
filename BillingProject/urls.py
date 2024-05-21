"""
URL configuration for BillingProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from billApp import views
from billApp import reports
urlpatterns = [
    path("admin/", admin.site.urls),
    path("invoice/", views.invoice_view),
    path("", views.hompageView),
    path("report/", views.plot_view),
    path("sign-in/", views.sign_in_page_view, name='sign_in'),
    path("welcome/", views.sign_in_view, name='process_email'),
    path("userdetails/", views.input_user_details_view, name='user_address'),
    path("addproduct/<str:string1>/", views.add_product_view, name='user_products'),
    path('generate-invoice/<str:mob_no>/', views.generate_invoice_view, name='generate_invoice'),
    path('customer-details/<str:mob_no>/', views.customer_details_view, name='customer_details'),
    path('transaction-details/<str:mob_no>/', views.transaction_details_view, name='transaction_details'),
    path('reports/<str:user_id>/', reports.reports_view, name='reports_view'),
    path("help/", views.help_view, name='help_page'),
]

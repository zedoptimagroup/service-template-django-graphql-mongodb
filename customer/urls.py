from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path("create"
         , views.create_customer
         , name="create_customer")
    , path("<str:customerId>/read"    
           , views.read_customer
           , name="read_customer")
    , path("<str:customerId>/update"
           , views.update_customer
           , name="update_customer")
    , path("<str:customerId>/delete"
           , views.delete_customer 
           , name="delete_customer")
]
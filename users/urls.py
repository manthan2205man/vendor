from django.urls import path
from .views.user_views import *
from .views.vendor_views import *
from .views.purchas_order_views import *


urlpatterns = [

    # Auth User APIS
    path('users/login/', UserLoginView.as_view()),
    path('users/', UserCreateView.as_view()),

    path('vendors/', CreateListVendorView.as_view()),
    path('vendors/<int:id>/', DeleteDetailUpdateVendorView.as_view()),
    path('vendors/<int:id>/performance/', PerformanceVendorView.as_view()),

    path('purchase_orders/', CreateListPurchaseOrderView.as_view()),
    path('purchase_orders/<int:id>/', DeleteDetailUpdatePurchaseOrderView.as_view()),

]
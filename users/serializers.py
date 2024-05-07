from rest_framework.serializers import ModelSerializer, Serializer
from . models import *
from rest_framework import serializers


# User Create Serializer
class UserCreateSerializer(ModelSerializer):

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


# Login Serializer
class UserLoginSerializer(ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']


# User Detail Serializer
class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

# Vendor Serializer
class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


# Purchase Order Serializer
class PurchaseOrderSerializer(ModelSerializer):

    class Meta:
        model =PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
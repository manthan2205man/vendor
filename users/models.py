from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Common Information Model 
class CommonInfo(models.Model):

    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        abstract=True


# User Model
class User(AbstractUser, CommonInfo):

    def __str__(self):
        return str(self.email) + ' - id - ' + str(self.id)
    
    class Meta:
        db_table = "users"


# User token Model
class UserToken(CommonInfo):

    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null= True)
    token = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return str(self.user) + ' UserTokenID ' + str(self.id)
    
    class Meta:
        db_table = "user_tokens"


# Vendor Model
class Vendor(CommonInfo):

    name = models.CharField(null=True, blank=True, max_length=200)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(null=True, blank=True, max_length=50)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + ' - id - ' + str(self.id)
    
    class Meta:
        db_table = "vendors"


# Purchase Order Model
class PurchaseOrder(CommonInfo):

    status_type = (
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('canceled', 'canceled'),
    )

    po_number = models.CharField(null=True, blank=True, max_length=50)
    vendor = models.ForeignKey(Vendor, related_name="purchas_orders", on_delete=models.CASCADE, null= True, blank=True)
    order_date = models.DateTimeField(null=True, auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(default=dict, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, max_length=20, choices=status_type)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.po_number) + ' - id - ' + str(self.id)
    
    class Meta:
        db_table = "purchas_orders"


# Historical Performance Model 
class HistoricalPerformance(CommonInfo):

    vendor = models.ForeignKey(Vendor, related_name="historical_performances", on_delete=models.CASCADE, null= True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.vendor) + ' - id - ' + str(self.id)
    
    class Meta:
        db_table = "historical_performances"
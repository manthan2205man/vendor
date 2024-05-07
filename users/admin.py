from django.contrib import admin
from . models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display  = ['email', 'id']
    # list_filter = ['is_delete']
admin.site.register(User, UserAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display  = ['name', 'id']
    list_filter = ['is_delete']
admin.site.register(Vendor, VendorAdmin)

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display  = ['po_number', 'id']
    list_filter = ['is_delete']
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display  = ['vendor', 'id']
    list_filter = ['is_delete']
admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)
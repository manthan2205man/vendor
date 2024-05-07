from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from django.utils import timezone
from django.db.models import Avg, Count

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, created, **kwargs):
    vendor = instance.vendor
    # Update on-time delivery rate
    if instance.status == 'completed':
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_orders = completed_orders.count()
        on_time_orders = completed_orders.filter(delivery_date__lte=instance.delivery_date)
        on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100 if total_completed_orders != 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
    # Update quality rating average
    quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(avg_quality=Avg('quality_rating'))
    vendor.quality_rating_avg = quality_rating_avg['avg_quality'] if quality_rating_avg['avg_quality'] else 0
    # Update fulfillment rate
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    successful_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    fulfillment_rate = (successful_orders / total_orders) * 100 if total_orders != 0 else 0
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    from django.db.models import ExpressionWrapper, F, DurationField

    vendor = instance.vendor
    if instance.acknowledgment_date:
        total_response_time = PurchaseOrder.objects.filter(
    acknowledgment_date__isnull=False,
    issue_date__isnull=False
).annotate(
    time_difference=ExpressionWrapper(
        F('acknowledgment_date') - F('issue_date'),
        output_field=DurationField()
    )
).aggregate(
    avg_response_time=Avg('time_difference')
)['avg_response_time']
        vendor.average_response_time = total_response_time.seconds if total_response_time else 0
        vendor.save()

@receiver(pre_delete, sender=PurchaseOrder)
def delete_update_vendor_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    # Recalculate performance metrics after deletion
    update_vendor_performance_metrics(sender, instance, created=False)

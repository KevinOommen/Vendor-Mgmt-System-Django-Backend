from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=instance.delivery_date).count()
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        if completed_pos.exists():
            quality_rating_avg = completed_pos.aggregate(avg_quality_rating=models.Avg('quality_rating'))['avg_quality_rating']
            vendor.quality_rating_avg = quality_rating_avg
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def calculate_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
        if completed_pos.exists():
            total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() / 3600 for po in completed_pos)
            average_response_time = total_response_time / completed_pos.count()
            vendor.average_response_time = average_response_time
            vendor.save()


@receiver(pre_save, sender=PurchaseOrder)
def calculate_fulfillment_rate(sender, instance, **kwargs):
    if instance.status_changed() or instance.pk is None:
        vendor = instance.vendor
        total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        fulfilled_pos = completed_pos.filter(quality_rating__isnull=False)
        if total_pos > 0:
            fulfillment_rate = (fulfilled_pos.count() / total_pos) * 100
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()

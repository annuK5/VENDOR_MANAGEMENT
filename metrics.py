from django.db.models import Avg, F, Count
from django.db.models.functions import Coalesce
from .models import PurchaseOrder


def calculate_on_time_delivery_rate(vendor):
    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    on_time_delivered_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        delivery_date__lte=Coalesce(F('acknowledgment_date'), F('delivery_date'))
    ).count()

    return (on_time_delivered_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0


def calculate_quality_rating_avg(vendor):
    result = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).aggregate(avg_quality_rating=Avg('quality_rating'))
    return result['avg_quality_rating'] or 0


def calculate_average_response_time(vendor):
    result = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        acknowledgment_date__isnull=False
    ).aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))

    avg_response_time = result['avg_response_time'] or 0

    return avg_response_time.total_seconds() / 3600 if avg_response_time else 0


def calculate_fulfillment_rate(vendor):
    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    fulfilled_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        quality_rating__isnull=True
    ).count()

    return (fulfilled_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0

from rest_framework import serializers
from .models import Vendor, PurchaseOrder
from django.utils import timezone

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
class VendorPerformanceSerializer(serializers.Serializer):
    on_time_delivery_rate = serializers.FloatField()
    quality_rating_avg = serializers.FloatField()
    average_response_time = serializers.FloatField()
    fulfillment_rate = serializers.FloatField()
class AcknowledgePurchaseOrderSerializer(serializers.Serializer):
    acknowledgment_date = serializers.DateTimeField(required=False, default=timezone.now)
    def validate_acknowledgment_date(self, value):
        return value
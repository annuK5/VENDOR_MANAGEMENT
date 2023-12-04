from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg
from .serializers import VendorSerializer, PurchaseOrderSerializer,VendorPerformanceSerializer,AcknowledgePurchaseOrderSerializer
from rest_framework import status 
from django.db.models import F
from django.http import JsonResponse
from .models import Vendor, PurchaseOrder
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .metrics import (calculate_on_time_delivery_rate,calculate_quality_rating_avg,calculate_average_response_time,calculate_fulfillment_rate)



class VendorListCreateView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorRetrieveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Response({"detail": "Vendor not found with the given ID."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderListCreateView(APIView):
    def get(self, request, format=None):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderRetrieveUpdateDeleteView(APIView):
    def get_object(self, po_number):
        try:
            return PurchaseOrder.objects.get(po_number=po_number)
        except PurchaseOrder.DoesNotExist:
            raise Response({"detail": "Purchase Order not found with the given po_number."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, po_number, format=None):
        po = self.get_object(po_number)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data)

    def put(self, request, po_number, format=None):
        po = self.get_object(po_number)
        serializer = PurchaseOrderSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_number, format=None):
        po = self.get_object(po_number)
        po.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_avg(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        performance_data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }

        return JsonResponse(performance_data)
    
class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = AcknowledgePurchaseOrderSerializer(data=request.data)

        if serializer.is_valid():
            acknowledgment_date = serializer.validated_data.get('acknowledgment_date', timezone.now())

            purchase_order.acknowledgment_date = acknowledgment_date
            purchase_order.save()

            vendor = purchase_order.vendor
            vendor.average_response_time = calculate_average_response_time(vendor)
            vendor.save()

            return Response({'message': 'Purchase order acknowledged successfully'})
        else:
            return Response({'error': 'Invalid data'}, status=400)
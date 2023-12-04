from django.urls import path
from .views import (
    VendorListCreateView,
    VendorRetrieveUpdateDeleteView,
    PurchaseOrderListCreateView,
    PurchaseOrderRetrieveUpdateDeleteView,
    VendorPerformanceView,AcknowledgePurchaseOrderView
)

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<str:po_number>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
]

from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDestroyView
from .views import PurchaseOrderListCreateView, PurchaseOrderRetrieveUpdateDestroyView

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),
    path('purchase-orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase-orders/<str:pk>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceMetricsAPIView.as_view(), name='vendor-performance-metrics'),
]

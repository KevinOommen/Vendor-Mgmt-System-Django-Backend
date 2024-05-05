from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderSerializer
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_code = self.request.query_params.get('vendor_code')
        if vendor_code:
            vendor = get_object_or_404(Vendor, pk=vendor_code)
            queryset = queryset.filter(vendor=vendor)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

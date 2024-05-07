from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json
from ..serializers import VendorSerializer
from ..models import Vendor
from users.utils import custom_pagination
from rest_framework import status
from django.db.models import Q, Value, Count, TextField
from django.db.models.functions import Concat

# Create your views here.

# Create & List Vendor View
class CreateListVendorView(GenericAPIView):
    serializer_class = VendorSerializer

    # permission_classes = [AllowAD]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "detail": serializer.errors,
                                  'data':{}},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            
            serializer.save()
            vendor = Vendor.objects.get(id=serializer.data['id'])
            vendor.vendor_code = 'VC' + str(vendor.id)
            vendor.save()
            return Response(data={"status": status.HTTP_201_CREATED,
                                    "detail": "Vendor Created Successfully.",
                                    "data": serializer.data},
                            status=status.HTTP_201_CREATED)

    # permission_classes = [AllowAD]
    def get(self, request):
        vats_search = ''
        search = request.GET.get('search')
        if search:
            vats_search = str(search)
        
        filter = request.GET.get('filter')
        if not filter:
            filter = {}
        if filter:
            filter = json.loads(filter)

        exclude = request.GET.get('exclude')
        if not exclude:
            exclude = {}
        if exclude:
            exclude = json.loads(exclude)


        sort = request.GET.get('sort')
        if not sort:
            sort = '-id'

        vendor = Vendor.objects.filter(is_delete=False, **filter).exclude(**exclude).order_by(sort).distinct()

        count = vendor.count()
        page_number = request.GET.get('page_number')
        page_size = request.GET.get('page_size')
        if not page_size:
            page_size = count

        vendor_obj = custom_pagination(page_number, page_size, vendor)
        serializer = self.get_serializer(vendor_obj, many=True)
        vendor_data = serializer.data

        vendor_data = {'count' : count,
                'results' : vendor_data}
        return Response(data={"status": status.HTTP_200_OK,
                                "detail": "Vendors list get successfully.",
                                'data':vendor_data},
                        status=status.HTTP_200_OK)


# Delete, Detail & Update Vendor View
class DeleteDetailUpdateVendorView(GenericAPIView):
    serializer_class = VendorSerializer

    # permission_classes = [AllowAD]
    def delete(self,request, id):
        vendor = Vendor.objects.filter(id=id, is_delete=False).first()
        if not vendor:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Vendor not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)
       
        vendor.is_delete=True
        vendor.save()
        return Response(data={"status": status.HTTP_204_NO_CONTENT,
                              "detail": 'Vendor deleted successfully.',
                              "data":{}},
                        status=status.HTTP_200_OK)

    # permission_classes = [AllowAD]
    def get(self,request,id):
        vendor = Vendor.objects.filter(id=id, is_delete=False).first()
        if not vendor:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Vendor not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(vendor)
        
        return Response(data={"status": status.HTTP_200_OK,
                                "detail": "Vendor get Successfully.",
                                "data": serializer.data},
                        status=status.HTTP_200_OK)

    # permission_classes = [AllowAD]
    def put(self,request,id):
        vendor = Vendor.objects.filter(id=id, is_delete=False).first()
        if not Vendor:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Vendor not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor, data=request.data)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "detail": serializer.errors,
                                  'data':{}},
                            status=status.HTTP_400_BAD_REQUEST)

        else:

            serializer.save()

            return Response(data={"status": status.HTTP_200_OK,
                                    "detail": "Vendor Updated Successfully.",
                                    "data": serializer.data},
                            status=status.HTTP_200_OK)


# Performance Vendor View
class PerformanceVendorView(GenericAPIView):
    serializer_class = VendorSerializer

    # permission_classes = [AllowAD]
    def get(self,request, id):
        vendor = Vendor.objects.filter(id=id, is_delete=False).first()
        if not vendor:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Vendor not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)
       
        vendor_performance = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }

        return Response(data={"status": status.HTTP_204_NO_CONTENT,
                              "detail": 'Vendor Performance get successfully.',
                              "data":vendor_performance},
                        status=status.HTTP_200_OK)

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json
from ..serializers import PurchaseOrderSerializer
from ..models import PurchaseOrder
from users.utils import custom_pagination
from rest_framework import status
from django.db.models import Q, Value, Count, TextField
from django.db.models.functions import Concat

# Create your views here.

# Create & List PurchaseOrder View
class CreateListPurchaseOrderView(GenericAPIView):
    serializer_class = PurchaseOrderSerializer

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
            purchase_order = PurchaseOrder.objects.get(id=serializer.data['id'])
            purchase_order.po_number = 'PO' + str(purchase_order.id)
            purchase_order.save()
            serializer = self.get_serializer(purchase_order)
            return Response(data={"status": status.HTTP_201_CREATED,
                                    "detail": "Purchase Order Created Successfully.",
                                    "data": serializer.data},
                            status=status.HTTP_201_CREATED)

    # permission_classes = [AllowAD]
    def get(self, request):
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

        purchase_order = PurchaseOrder.objects.filter(is_delete=False, **filter).exclude(**exclude).order_by(sort).distinct()

        count = purchase_order.count()
        page_number = request.GET.get('page_number')
        page_size = request.GET.get('page_size')
        if not page_size:
            page_size = count

        purchase_order_obj = custom_pagination(page_number, page_size, purchase_order)
        serializer = self.get_serializer(purchase_order_obj, many=True)
        purchase_order_data = serializer.data

        purchase_order_data = {'count' : count,
                'results' : purchase_order_data}
        return Response(data={"status": status.HTTP_200_OK,
                                "detail": "Purchase Orders list get successfully.",
                                'data':purchase_order_data},
                        status=status.HTTP_200_OK)


# Delete, Detail & Update PurchaseOrder View
class DeleteDetailUpdatePurchaseOrderView(GenericAPIView):
    serializer_class = PurchaseOrderSerializer

    # permission_classes = [AllowAD]
    def delete(self,request, id):
        purchase_order = PurchaseOrder.objects.filter(id=id, is_delete=False).first()
        if not purchase_order:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Vendor not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)
       
        purchase_order.is_delete=True
        purchase_order.save()
        return Response(data={"status": status.HTTP_204_NO_CONTENT,
                              "detail": 'Purchase Order deleted successfully.',
                              "data":{}},
                        status=status.HTTP_200_OK)

    # permission_classes = [AllowAD]
    def get(self,request,id):
        purchase_order = PurchaseOrder.objects.filter(id=id, is_delete=False).first()
        if not purchase_order:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Purchase Order not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(purchase_order)
        
        return Response(data={"status": status.HTTP_200_OK,
                                "detail": "Purchase Order get Successfully.",
                                "data": serializer.data},
                        status=status.HTTP_200_OK)

    # permission_classes = [AllowAD]
    def put(self,request,id):
        purchase_order = PurchaseOrder.objects.filter(id=id, is_delete=False).first()
        if not purchase_order:
            return Response(data={"status": status.HTTP_404_NOT_FOUND,
                                  "detail": 'Purchase Order not found.',
                                  "data":{}},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "detail": serializer.errors,
                                  'data':{}},
                            status=status.HTTP_400_BAD_REQUEST)

        else:

            serializer.save()

            return Response(data={"status": status.HTTP_200_OK,
                                    "detail": "Purchase Order Updated Successfully.",
                                    "data": serializer.data},
                            status=status.HTTP_200_OK)



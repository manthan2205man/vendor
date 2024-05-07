from rest_framework.views import exception_handler
from rest_framework.authentication import get_authorization_header
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status'] = response.status_code
        response.data['data'] = {}
    
    
    # if response is None:
    #     return Response(
    #         data={
    #             "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             # "detail":"Internal server error",
    #             "detail":str(exc),
    #             "data":{}},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )

    return response


def Authenticate(self, request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'token':
        return None
    token = auth[1]
    return token


def custom_pagination(page_number, page_size, queryset):
    if not page_size:
        page_size = 20
        
    page = Paginator(queryset, page_size) 
    try:
        object = page.get_page(page_number)  
    except PageNotAnInteger:
        object = page.page(1)
    except EmptyPage:
        object = page.page(page.num_pages)

    return object

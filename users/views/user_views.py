from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import jwt, json
import string,random
from ..serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer
from ..models import User, UserToken
from ..utils import custom_pagination
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta, timezone
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

# Auth APIS
# User Login View
class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "detail": serializer.errors,
                                  "data":{}},
                            status= status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email, is_delete=False).exists()
        
        if not user:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                    "detail": "The credentials you entered are not valid. Please try again.",
                                    "data":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            # password hash
            user = User.objects.get(email=email, is_delete=False)
            new_password = check_password(password, user.password)
            # password hash
            if new_password == False:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                      "detail": "The password does not match, Please recheck.",
                                       "data":{}},
                                            status=status.HTTP_400_BAD_REQUEST)

            if user.is_active == False:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                      "detail": "User is not active, Please make sure user is active.",
                                      "data":{}},
                                            status=status.HTTP_400_BAD_REQUEST)
            
            # allow only one "session" per user
            token = UserToken.objects.filter(user_id=user.id, is_delete = False).order_by("-updated_at").first()
            if token and not settings.DEBUG:
                token.is_delete=True
                token.save()

            dt = datetime.now(tz=timezone.utc) + timedelta(days=10)           
            letters = string.ascii_letters
            random_string = ''.join(random.choice(letters) for i in range(15))
            payload = {'exp': dt ,'id': user.id, 'email': email, 'random_string': random_string}
            encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            UserToken.objects.create(user=user, token=encoded_token)
            serializer = UserDetailSerializer(user)

            return Response(data={"status": status.HTTP_200_OK,
                                    "detail": "User successfully login, Token Generated.",
                                    "data": {'token': encoded_token,
                                         'user_data':serializer.data}},
                            status= status.HTTP_200_OK)
    

# User create API View
class UserCreateView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "detail": serializer.errors,
                                  "data":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']

        if User.objects.filter(email=email, is_delete=True).exists():
            User.objects.get(email=email, is_delete=True).delete()

        if User.objects.filter(email=email, is_delete=False).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "detail": "User Email Already Registered.",
                                  "data":{}},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            # password hash
            password = serializer.validated_data['password']
            hash_password = make_password(password)
            # password hash
            serializer.validated_data['password'] = hash_password
            serializer.validated_data['username'] = email
            serializer.save()
            user = User.objects.get(email=email, is_delete=False)
            serializer = UserDetailSerializer(user)
            return Response(data={"status": status.HTTP_201_CREATED,
                                    "detail": "User created successfully.",
                                    "data": serializer.data},
                            status=status.HTTP_201_CREATED)

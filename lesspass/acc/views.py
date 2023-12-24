
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from rest_framework.views import APIView
from .serializers import GetPhoneNumberSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from utils.send_otp import send_otp
from utils.get_code import get_otp_code




class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None


class GetCodeView(APIView):

    
    def post(self, request, *args, **kwargs):
       serializer = GetPhoneNumberSerializer(data=request.data)

       if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = get_user_model().objects.get_or_create(phone_number=phone_number, is_active=True)
            if user:
                code = get_otp_code(user[0])
                send_otp(phone_number, code)
                return Response({'message': 'OTP Code sent successfully.'}, status=status.HTTP_200_OK)
       else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import GetPhoneNumberSerializer, LoginSerializer
from .tasks import send_otp_to_phone_number_task
from utils.get_code import generate_otp_code
from core.logger import logger
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class GetCodeView(APIView):
    """
    API view for getting OTP code based on the provided phone number.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to generate and send OTP code.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: HTTP response with the result of OTP code generation and sending.
        """
        # Validate input data
        serializer = GetPhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract phone number from validated data
        phone_number = serializer.validated_data["phone_number"]

        # Get or create user based on the phone number
        user, created = get_user_model().objects.get_or_create(
            phone_number=phone_number, is_active=True
        )

        if created:
            logger.info(f"User created with phone number: {phone_number}")

        # Generate OTP code and send it asynchronously
        otp_code = generate_otp_code(user)
        send_otp_to_phone_number_task.delay(phone_number, otp_code)
        print("*" * 10, otp_code)
        return Response(
            {"message": "OTP Code sent successfully."}, status=status.HTTP_200_OK
        )


class LandingPageView(TemplateView):
    template_name = "landing-page.html"

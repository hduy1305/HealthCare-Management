# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import User

# 1. Đăng ký
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# 2. Login trả về JWT tokens
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

# 3. Lấy thông tin user hiện tại
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

# Ví dụ 1 view chỉ cho Admin truy cập
from .permissions import IsAdmin
class AdminOnlyView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()

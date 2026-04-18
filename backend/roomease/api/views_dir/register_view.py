from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers_dir.user_serializer import RegisterSerializer,LoginSerializer
from rest_framework import status

class RegisterView(APIView):
    def post(self,request):
        data = request.data
       
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"data":serializer.data},status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self,request):
        print("am i here though")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh_token':str(refresh),
                    'access_token':str(refresh.access_token)
            })
        return Response({'success':False,
                         "message":"Invalid Credentials"},status=401)
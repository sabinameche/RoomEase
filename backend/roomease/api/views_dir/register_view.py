from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers_dir.user_serializer import UserSerializer
from rest_framework import status

class RegisterView(APIView):
    def post(self,request):
        data = request.data
        print("printing data",data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"data":serializer.data},status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
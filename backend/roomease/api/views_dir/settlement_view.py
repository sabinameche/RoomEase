from ..serializers_dir.settlement_serializer import SettlementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SettlementView(APIView):
    def post(self,request,id):
        data = request.data.copy()
        data['group'] = id
        data['settled_by'] = request.user.id
        serializer = SettlementSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"settlement":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"success":False,"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
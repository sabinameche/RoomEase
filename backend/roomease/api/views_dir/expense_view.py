from rest_framework.views import APIView
from ..serializers_dir.expense_serializers import ExpenseSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal

class ExpenseView(APIView):
    def get(self,request,id):
        group = Group.objects.get(id =id)
        expenses = Expense.objects.filter(group = group)
        serializer = ExpenseSerializer(expenses,many = True)
        
        return Response({"success":True,"data":serializer.data})
        


    @transaction.atomic
    def post(self,request,id):
        data = request.data.copy()
        
        data["group"] = id
        serializer = ExpenseSerializer(data = data)

        if serializer.is_valid():
        
            serializer.save()
            return Response({"success":True,"data":serializer.data})
        return Response({"success":False,"errors":serializer.errors})
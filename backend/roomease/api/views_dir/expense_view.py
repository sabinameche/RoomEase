from rest_framework.views import APIView
from ..serializers_dir.expense_serializers import ExpenseSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal
from rest_framework import status
from ..services.expense_split_services import ExpenseSplitService
from ..services.expense_owned_services import ExpenseOwnedService

class ExpenseView(APIView):
    def get(self,request,expense,id):
        if expense == 'all':
            group = Group.objects.get(id =id)
            expenses = Expense.objects.filter(group = group).order_by("-created_at")
            serializer = ExpenseSerializer(expenses,many = True)
            expense_per_user = ExpenseOwnedService.expense_per_user(id)
            return Response({"success":True,"data":serializer.data,"expense_per_user":expense_per_user},status=status.HTTP_200_OK)
        
        elif expense == 'specific':
            try:
                expenses = Expense.objects.get(id = id)
                serializer = ExpenseSerializer(expenses)
        
        
                return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
            except:
                return Response({"success":False},status=status.HTTP_404_NOT_FOUND)
        


    @transaction.atomic
    def post(self,request,id):
        data = request.data.copy()
        
        data["group"] = id
        data['created_by'] = request.user.id
    
        serializer = ExpenseSerializer(data = data)

        if serializer.is_valid():
        
            serializer.save()
            return Response({"success":True,"data":serializer.data},status= status.HTTP_201_CREATED)
        return Response({"success":False,"errors":serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self,request,id):
    
        expense = Expense.objects.get(id= id)
        data = request.data
        split_type = data.get("split_type")
        total_amount = data.get("amount")
        participants = data.pop("participants")
        if request.user == expense.created_by or request.user == expense.expense_group.user:
        
            serializer = ExpenseSerializer(expense,data = data,partial=True)

            if serializer.is_valid():
                serializer.save()
                
                ExpenseSplitService.update_expense_split(expense,participants,split_type,total_amount)
                return Response({'success':True,'message':'Expense updated successfully','data':serializer.data},
                                status=status.HTTP_200_OK)
            return Response({'success':False,
                            'error':serializer.errors,
                            },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':False,"error":"You're not authorized to update"},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        expense = Expense.objects.get(id=id)
        if request.user == expense.created_by or request.user == expense.expense_group.user:
            expense.delete()
            return Response({'success':True,'message':'Expense deleted successfully'},status=status.HTTP_200_OK)
        return Response({'success':False,'message':"You're not authorized to delete!"},status=status.HTTP_401_UNAUTHORIZED)
        

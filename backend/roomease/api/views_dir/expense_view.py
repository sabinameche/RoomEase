from rest_framework.views import APIView
from ..serializers_dir.expense_serializers import ExpenseSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal
from rest_framework import status

class ExpenseView(APIView):
    def get(self,request,expense,id):
        if expense == 'total':
            group = Group.objects.get(id =id)
            expenses = Expense.objects.filter(group = group,is_deleted = False).order_by("-created_at")
            serializer = ExpenseSerializer(expenses,many = True)
        elif expense == 'single':
            expenses = Expense.objects.get(id = id)
            serializer = ExpenseSerializer(expenses)
        
        return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
        


    @transaction.atomic
    def post(self,request,id):
        data = request.data.copy()
        print('value aayo data',data)
        
        data["group"] = id
        data['created_by'] = request.user.id
    
        serializer = ExpenseSerializer(data = data)

        if serializer.is_valid():
        
            serializer.save()
            return Response({"success":True,"data":serializer.data},status= status.HTTP_201_CREATED)
        return Response({"success":False,"errors":serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self,request,id):
    
        expense = Expense.objects.get(id= id)
        if request.user == expense.created_by or request.user == expense.expense_group.user:
            print('data aako k k xa tw yaa heram haii tw',request.data)
        
            serializer = ExpenseSerializer(expense,data = request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
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
            expense.is_deleted = True
            expense.save()
            return Response({'success':True,'message':'Expense deleted successfully'},status=status.HTTP_200_OK)
        return Response({'success':False,'message':"You're not authorized to delete!"},status=status.HTTP_401_UNAUTHORIZED)
        

from rest_framework.views import APIView
from rest_framework import serializers
from ..serializers_dir.expenseSplit_serializer import ExpenseSplitSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from decimal import Decimal

class ExpenseSplitService:

    def create_expense_split(expense,participants,validated_data):
    
        split_type = validated_data.get('split_type')
        if split_type == "EQUAL":
            for user_id in participants:
                print('ma loop ma xu??')
                user = CustomUser.objects.get(id = user_id)

                ExpenseSplit.objects.create(expense = expense,user=user,amount = Decimal(expense.amount)/Decimal(len(participants)))


        elif split_type == "PERCENTAGE":
            total_percentage = sum(participants.values())
        
            if total_percentage !=100:
                raise serializers.ValidationError("Percentage should be equal to 100")
            
            for user_id in participants:
    
                user = CustomUser.objects.get(id=int(user_id))

                ExpenseSplit.objects.create(expense = expense,user=user,amount=(Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100))

        elif split_type == "EXACT":
            sum_amount = sum(participants.values())
            total_amount = validated_data.get('amount')
            if sum_amount == total_amount:
                raise serializers.ValidationError("Total amount should be equal to the sum of amount!")
            
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                ExpenseSplit.objects.create(expense=expense,user=user,amount = Decimal(participants[user_id]))
       

    def update_expense_split(expense,participants,validated_data):
       
        ExpenseSplit.objects.filter(expense = expense).delete()
        ExpenseSplitService.create_expense_split(expense,participants,validated_data)
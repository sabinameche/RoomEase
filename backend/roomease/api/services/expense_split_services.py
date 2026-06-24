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
                user = CustomUser.objects.get(id = user_id)
                
                expense_split,created = ExpenseSplit.objects.update_or_create(expense = expense,user=user,defaults={'user':user,'amount' : Decimal(expense.amount)/Decimal(len(participants))})


        elif split_type == "PERCENTAGE":
            total_percentage = sum(participants.values())
            print('participants ma kei xaina rw',participants)
            if total_percentage !=100:
                raise serializers.ValidationError("Percentage should be equal to 100")
            
            for user_id in participants:
    
                user = CustomUser.objects.get(id=int(user_id))

                expense_split,created=ExpenseSplit.objects.update_or_create(expense = expense,user=user,defaults={'user':user,'amount':(Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100)})

        elif split_type == "EXACT":
            sum_amount = sum(participants.values())
            total_amount = validated_data.get('amount')
            if sum_amount == total_amount:
                raise serializers.ValidationError("Total amount should be equal to the sum of amount!")
            
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                expense_split,created=ExpenseSplit.objects.update_or_create(expense=expense,user=user,defaults={'amount' : Decimal(participants[user_id])})
        return expense_split
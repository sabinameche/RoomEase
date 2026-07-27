from rest_framework.views import APIView
from rest_framework import serializers
from ..serializers_dir.expenseSplit_serializer import ExpenseSplitSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense,OwnedAmount
from rest_framework.response import Response
from decimal import Decimal

class ExpenseSplitService:

    def create_expense_split(expense,participants,split_type,total_amount,group):
    
        if split_type == "EQUAL":
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)

                expense_split = ExpenseSplit.objects.create(expense = expense,user=user,amount = Decimal(expense.amount)/Decimal(len(participants)))

                # calculating user's total owed money
                owes,created = OwnedAmount.objects.get_or_create(group = group,user = user,
                                                                     defaults={'group' :group,
                                                                               'user': user,
                                                                               'amount' : 0})
                owes.amount += expense_split.amount
                owes.save()


        elif split_type == "PERCENTAGE":
            total_percentage = sum(participants.values())
        
            if total_percentage !=100:
                raise serializers.ValidationError("Percentage should be equal to 100")
            
            for user_id in participants:
    
                user = CustomUser.objects.get(id=int(user_id))

                expense_split = ExpenseSplit.objects.create(expense = expense,user=user,amount=(Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100))
                # calculating user's total owed money
                owes,created = OwnedAmount.objects.get_or_create(group = group,user = user,
                                                                     defaults={'group' :group,
                                                                               'user': user,
                                                                               'amount' : 0})
                owes.amount += expense_split.amount
                owes.save()

        elif split_type == "EXACT":
            sum_amount = sum(participants.values())
        
            if sum_amount == total_amount:
                raise serializers.ValidationError("Total amount should be equal to the sum of amount!")
            
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                expense_split = ExpenseSplit.objects.create(expense=expense,user=user,amount = Decimal(participants[user_id]))

                # calculating user's total owed money
                owes,created = OwnedAmount.objects.get_or_create(group = group,user = user,
                                                                     defaults={'group' :group,
                                                                               'user': user,
                                                                               'amount' : 0})
                owes.amount += expense_split.amount
                owes.save()
       

    def update_expense_split(expense,participants,split_type,total_amount):
       
        ExpenseSplit.objects.filter(expense = expense).delete()
        print('feri delete vara create chai kina navako k')
        ExpenseSplitService.create_expense_split(expense,participants,split_type,total_amount)
from rest_framework.views import APIView
from rest_framework import serializers
from ..serializers_dir.expenseSplit_serializer import ExpenseSplitSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from decimal import Decimal
from django.db.models import Sum

# calculate expenses amount owned per user
class ExpenseOwnedService:
    def expense_per_user(groupId):
        #calculate amount owes per user
    
        expense_split = ExpenseSplit.objects.filter(expense__group_id = groupId).values("user__username").annotate(total=Sum("amount"))

        #calculate amount paidby user
        expense = Expense.objects.filter(group = groupId).values("paid_by__username").annotate(paid_total = Sum("amount"))
        print('amount paid vako user bata',expense)

        exp_dict = {}
        for exp in expense:
            
            exp_dict[exp["paid_by__username"]] = exp["paid_total"]
        
        user_expense_owes = []

        #calculate the amount after subtracting what they paid and what they owes
        for user in expense_split:
            user_owes = {}
          
            if user["user__username"] in exp_dict:
                
                amount_owes = user["total"] - exp_dict[user["user__username"]]
                user_owes["name"] = user["user__username"]
                user_owes["amount"] = amount_owes
            else:
                user_owes["name"] = user["user__username"]
                user_owes["amount"] = user["total"]
            user_expense_owes.append(user_owes)
       
        return user_expense_owes
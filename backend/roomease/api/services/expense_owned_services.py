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
        expense_split = ExpenseSplit.objects.filter(expense__group_id = groupId).values("user__username").annotate(total=Sum("amount"))
        expense = Expense.objects.filter(group = groupId).values("paid_by__username").annotate(paid_total = Sum("amount"))
        exp_dict = {}
        for exp in expense:
            
            exp_dict[exp["paid_by__username"]] = exp["paid_total"]
        print('exp dictionary ma heram ',exp_dict)
           
        user_owes = {}


        for user in expense_split:
            
            if user["user__username"] in exp_dict:
                amount_owes = user["total"] - exp_dict[user["user__username"]]
                user_owes[user["user__username"]] = amount_owes
            else:
                user_owes[user["user__username"]] = user["total"]
                print('kati amount ow garyo',amount_owes)
        print(user_owes)
        return user_owes
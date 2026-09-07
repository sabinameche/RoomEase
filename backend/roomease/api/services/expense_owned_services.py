from rest_framework.views import APIView
from rest_framework import serializers
from ..serializers_dir.expenseSplit_serializer import ExpenseSplitSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from decimal import Decimal
from django.db.models import Sum
from operator import itemgetter

# calculate expenses amount owned per user
class ExpenseOwnedService:

    def calculate_net_balance_per_user(groupId):

        # amount they owes per user after split
        amount_per_user = ExpenseSplit.objects.filter(expense__group = groupId).values('user__id').annotate(total_owes =Sum('amount'))
        
        # amount per user paid
        
        paid_per_user = Expense.objects.filter(group = groupId).values('paid_by').annotate(total_paid = Sum('amount'))

        paid_by_user = {}
        for per_user in paid_per_user:
            paid_by_user[per_user['paid_by']] = per_user['total_paid']
        
        net_balance ={}
        for amount_user in amount_per_user:
            if amount_user['user__id'] in paid_by_user:

                total_paid = paid_by_user[amount_user['user__id']]
                net_balance[amount_user['user__id']] = total_paid - amount_user['total_owes']

            else:
                total_paid = 0
                net_balance[amount_user['user__id']] = total_paid - amount_user['total_owes']

        user,max_balance = max(net_balance.items(),key=itemgetter(1))
        
        who_owes_whom ={}
        print('okay check items ma k xa',net_balance.items())
        for item,value in net_balance.items():
            if value != max_balance:
                if abs(value)<max_balance:
                    who_owes_whom[item] = user
                    
            print(item,value)
        return net_balance
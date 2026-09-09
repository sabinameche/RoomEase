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

    def calculate_net_balance_per_user(self,groupId):

        # amount they owes per user after split
        amount_per_user = ExpenseSplit.objects.filter(expense__group = groupId).values('user__id').annotate(total_owes =Sum('amount'))

        # amount per user paid
        
        paid_per_user = Expense.objects.filter(group = groupId).values('paid_by').annotate(total_paid = Sum('amount'))

        balance_per_user = {}
        for user in amount_per_user:
            balance_per_user[user['user__id']] = user['total_owes']

        creditor = {}
        debtor = {}
            
        paid_by_user = {}
        for per_user in paid_per_user:
           

            if per_user['paid_by'] not in balance_per_user:
                creditor[per_user['paid_by']] = per_user['total_paid']
                
            paid_by_user[per_user['paid_by']] = per_user['total_paid']
        
    
        for user in amount_per_user:

            if user['user__id'] in paid_by_user:

                total_paid = paid_by_user[user['user__id']]
                net_balance = total_paid - user['total_owes']

            else:
                total_paid = 0
                net_balance= total_paid - user['total_owes']

            if net_balance < 0:
                debtor[user['user__id']] = net_balance
            else:
                creditor[user['user__id']] = net_balance

        
        return debtor,creditor

    def who_pays_whom(self,groupId):
        settlement = []
        debtor,creditor = self.calculate_net_balance_per_user(groupId)
        debtor_keys = list(debtor.keys())
        creditor_keys = list(creditor.keys())
       
        i = 0
        j = 0
        
        while i  < len(debtor_keys) and j < len(creditor_keys):
                    
            deb_key = debtor_keys[i]
            cred_key = creditor_keys[j]

            if debtor[deb_key] ==0:
                i += 1
                continue
            if creditor[cred_key] ==0:
                j += 1
                continue

            settle_amount =  min(abs(debtor[deb_key]),creditor[cred_key])
            debtor[deb_key] += settle_amount
            creditor[cred_key] -= settle_amount
            settlement.append({'from':deb_key,'to':cred_key,'amount':settle_amount})
            
            if debtor[deb_key] == 0:
                i += 1
            if creditor[cred_key] == 0:
                j += 1
                          
        return settlement
        
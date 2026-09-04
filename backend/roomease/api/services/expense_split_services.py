from ..models import ExpenseSplit,CustomUser,Expense,OwnedAmount
from decimal import Decimal

class ExpenseSplitService:

    def create_expense_split(expense,participants,split_type):

        if split_type == "EQUAL":
            for user_id in participants:

                expense_split = ExpenseSplit.objects.create(expense = expense,user_id=user_id,amount = Decimal(expense.amount)/Decimal(len(participants)))

                # # calculating user's total owed money
                # owes,created = OwnedAmount.objects.get_or_create(group = group,user = user,
                #                                                      defaults={'group' :group,
                #                                                                'user': user,
                #                                                                'amount' : 0})
                # owes.amount += expense_split.amount
                # owes.save()
                
                # if user_id == paid_by:
                #     owes.amount -= total_amount
                #     owes.save()


        elif split_type == "PERCENTAGE":
            total_percentage = sum(participants.values())
        
            if total_percentage !=100:
                raise ValueError("Percentage should be equal to 100")
            
            for user_id in participants:
    
                expense_split = ExpenseSplit.objects.create(expense = expense,user_id=user_id,amount=(Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100))
                
                # calculating user's total owed money
                # owes,created = OwnedAmount.objects.get_or_create(group = group,user = user,
                #                                                      defaults={'group' :group,
                #                                                                'user': user,
                #                                                                'amount' : 0})
                # owes.amount += expense_split.amount
                # owes.save()
                
                # if int(user_id) == paid_by.id:

                #     owes = OwnedAmount.objects.get(group = group,user = paid_by.id)
                #     owes.amount -= total_amount
                #     owes.save()

        elif split_type == "EXACT":
            sum_amount = sum(participants.values())
            
            if sum_amount != expense.amount:
                raise ValueError("Total amount should be equal to the sum of amount!")
            
            for user_id in participants:
              
                expense_split = ExpenseSplit.objects.create(expense=expense,user_id=user_id,amount = Decimal(participants[user_id]))

                # calculating user's total owed money
                # owes,created = OwnedAmount.objects.get_or_create(group = group,user = user,
                #                                                      defaults={'group' :group,
                #                                                                'user': user,
                #                                                                'amount' : 0})
                # owes.amount += expense_split.amount
                # owes.save()
                # if user_id == paid_by:
                #     owes.amount -= total_amount
                #     owes.save()
       

    def update_expense_split(expense,participants,split_type):
       
        ExpenseSplit.objects.filter(expense = expense).delete()
        
        ExpenseSplitService.create_expense_split(expense,participants,split_type)
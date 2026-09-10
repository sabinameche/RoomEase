from ..models import ExpenseSplit,CustomUser,Expense
from decimal import Decimal

class ExpenseSplitService:

    def create_expense_split(expense,participants,split_type,paid_by):

        if split_type == "EQUAL":
            for user_id in participants:

                ExpenseSplit.objects.create(expense = expense,user_id=user_id,amount = Decimal(expense.amount)/Decimal(len(participants)))
            


        elif split_type == "PERCENTAGE":
            total_percentage = sum(participants.values())
        
            if total_percentage !=100:
                raise ValueError("Percentage should be equal to 100")
            
            for user_id in participants:
    
                ExpenseSplit.objects.create(expense = expense,user_id=user_id,amount=(Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100))
                

        elif split_type == "EXACT":
            sum_amount = sum(participants.values())
            
            if sum_amount != expense.amount:
                raise ValueError("Total amount should be equal to the sum of amount!")
            
            for user_id in participants:
              
                ExpenseSplit.objects.create(expense=expense,user_id=user_id,amount = Decimal(participants[user_id]))
       

    def update_expense_split(expense,participants,split_type):
       
        ExpenseSplit.objects.filter(expense = expense).delete()
        
        ExpenseSplitService.create_expense_split(expense,participants,split_type)
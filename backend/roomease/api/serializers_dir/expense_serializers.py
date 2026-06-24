from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from ..models import Expense,Group,ExpenseSplit,CustomUser
from decimal import Decimal
from django.db import transaction

class ExpenseSerializer(ModelSerializer):
    participants = serializers.DictField(child=serializers.IntegerField(),write_only = True)

    user_name = serializers.CharField(source = "paid_by.username",read_only = True)
    class Meta:
        model = Expense
        read_only_fields = ["id"]
        fields = ["id","group","title","amount","paid_by","participants","user_name","category","created_by","split_type"]
        
    
    def validate(self,data):
        group = data.get("group")
        participants =data.get("participants")
        amount = data.get("amount")
        paid_by = data.get("paid_by")
        
        # check if list is empty
        if participants != None:
            if not participants:
                raise serializers.ValidationError("Pariticipants list cannot be empty.")
            
            # check if duplicate id
            if len(participants) != len(set(participants)):
                raise serializers.ValidationError("Duplicate Id is not allowed.")
            
            # check if the id is correct
            group_member_user_id = str(set(group.members.values_list("user_id", flat=True)))
         
            for user_id in participants:
                if user_id not in group_member_user_id:
                    raise serializers.ValidationError(
                        f"User {user_id} is not a member of this group."
                    )

            #check the amount
            if amount <=0:
                raise serializers.ValidationError("The amount must be greater than 0")
            
            # check if paid_by in group 
            if str(paid_by.id) not in group_member_user_id:
                raise serializers.ValidationError(f"User {paid_by.id}{group_member_user_id} is not a member of this group")
        
        return data
    
    def create(self,validated_data):
        participants = validated_data.pop("participants")
        split_type = validated_data.get("split_type")
        expense = Expense.objects.create(**validated_data)

        if split_type == "EQUAL":
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                
                ExpenseSplit.objects.create(expense = expense,user=user,amount = Decimal(expense.amount)/Decimal(len(participants)))

        elif split_type == "PERCENTAGE":
            total_percentage = sum((participants.values()))
    
            if total_percentage !=100:
                raise serializers.ValidationError("Percentage should be equal to 100")
            
            for user_id in participants:
               
                user = CustomUser.objects.get(id=user_id)
                ExpenseSplit.objects.create(expense = expense,user=user,amount = (Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100))

        elif split_type == "EXACT":
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                ExpenseSplit.objects.create(expense=expense,user=user,amount = Decimal(participants[user_id]))
        return expense
    
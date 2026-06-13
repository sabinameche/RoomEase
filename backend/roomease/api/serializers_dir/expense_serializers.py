from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from ..models import Expense,Group,ExpenseSplit,CustomUser
from decimal import Decimal

class ExpenseSerializer(ModelSerializer):
    participants = serializers.ListField(child = serializers.IntegerField(),write_only = True)
    user_name = serializers.CharField(source = "paid_by.username")
    class Meta:
        model = Expense
        fields = ["group","title","amount","paid_by","participants","user_name"]
        read_only_field = ["user_name"]
    
    def validate(self,data):
        group = data.get("group")
        participants =data.get("participants",[])
        amount = data.get("amount")
        paid_by = data.get("paid_by")
        
        # check if list is empty
        if not participants:
            raise serializers.ValidationError("Pariticipants list cannot be empty.")
        
        # check if duplicate id
        if len(participants) != len(set(participants)):
            raise serializers.ValidationError("Duplicate Id is not allowed.")
        
        # check if the id is correct
        group_member_user_id = set(group.members.values_list("user_id", flat=True))
        for user_id in participants:
            if user_id not in group_member_user_id:
                raise serializers.ValidationError(
                    f"User {group_member_user_id}{user_id} is not a member of this group."
                )

        #check the amount
        if amount <=0:
            raise serializers.ValidationError("The amount must be greater than 0")
        
        # check if paid_by in group 
        if paid_by.id not in group_member_user_id:
            raise serializers.ValidationError(f"User {paid_by.id}{group_member_user_id} is not a member of this group")
        
        return data
    
    def create(self,validated_data):
        participants = validated_data.pop("participants")
        expense = Expense.objects.create(**validated_data)

        for user_id in participants:
            user = CustomUser.objects.get(id = user_id)
            
            ExpenseSplit.objects.create(expense = expense,user=user,amount = Decimal(expense.amount)/Decimal(len(participants)))
        return expense
    
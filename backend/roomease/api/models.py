from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_img",null= True,blank = True)

class Group(models.Model):
    
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=255,default="NPR")
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="created_groups")
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    ROLE_CHOICES = (
        ("admin","ADMIN"),
        ("member","MEMBER")
    )
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="members")
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default="member")
    joined_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
    
class GroupInvite(models.Model):
    STATUS_CHOICES = (
        ("pending","PENDING"),
        ("accepted","ACCEPTED"),
        ("rejected","REJECTED")
    )
    email = models.EmailField(max_length=255)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="invites")
    invited_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4,unique = True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="pending")
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Invite to {self.group.name} - {self.email}"
    
class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name="expense_group")
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="paid_by_user")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser,on_delete =  models.PROTECT,related_name='created_by_user')
    CATEGORY_CHOICES = {
        "GROCERIES" :"Groceries",
        "RENT": "Rent",
        "UTILITIES":"Utilites",
        "INTERNET":"Internet",
        "TRANSPORT":"Transport",
        "OTHER":"Other",
    }
    category = models.CharField(max_length= 20,choices=CATEGORY_CHOICES,default="")
    SPLIT_CHOICES={
        "EQUAL":"Equal",
        "PERCENTAGE":"Percentage",
        "EXACT":"Exact"
    }
    split_type = models.CharField(max_length= 20,choices=SPLIT_CHOICES,default="EQUAL")
   


class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
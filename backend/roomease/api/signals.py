from .models import GroupInvite
from django.dispatch import receiver
from django.db.models.signals import post_save
from .views_dir.group_invite_view import send_group_invite_email
@receiver(post_save,sender =GroupInvite)
def group_invite_created(sender,instance,created,**kwargs):
    if created:
        send_group_invite_email(instance)


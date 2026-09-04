from ..models import Group,GroupInvite,GroupMember,CustomUser
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers_dir.group_invite_serializer import GroupInviteSerializer
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect,HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
import hashlib
from django.core.cache import cache

def send_group_invite_email(invite):
    accept_link = f"http://localhost:8000/api/invite/accept/{invite.token}/"
    reject_link=f"http://localhost:8000/api/invite/reject/{invite.token}/"

    subject ="Group Invitation"
    html_content = f"""
        <h3>You're invited to join a group</h3>
        <a href="{accept_link}"
            style = "padding:10px 20px;background-color:green;color:white;text-decoration:none;border-radius:5px;">
        Accept
        </a>
        <br><br>
            <a href="{reject_link}"style = "padding:10px 20px;background-color:red;color:white;text-decoration:none;border-radius:5px;">
            Reject
            </a>
        """
    email = EmailMultiAlternatives(
            subject,
            "",
            settings.EMAIL_HOST_USER,
            [invite.email]
        )
        
    email.attach_alternative(html_content,"text/html")
    email.send(fail_silently=False)


class AcceptInvite(APIView):

    def get(self,request,token):

        invite = GroupInvite.objects.get(token=token)
        
        user = CustomUser.objects.filter(email = invite.email).first()

        if not user:
            return HttpResponseRedirect(f"http://127.0.0.1:5501/RoomEase/frontend/html/register.html?invite={invite.token}")
        else:
            if invite.status == "accepted":
                return HttpResponseRedirect(f"http://127.0.0.1:5501/RoomEase/frontend/html/login.html?invite={invite.token}")
            else:
                if invite.status == "rejected":
                    return HttpResponse("Invitation has already been rejected.")
                GroupMember.objects.get_or_create(user=user,group=invite.group,defaults={"user":user,"group":invite.group,"role":"member"})
                invite.status = "accepted"
                invite.save()
            
                return HttpResponseRedirect(f"http://127.0.0.1:5501/RoomEase/frontend/html/login.html?invite={invite.token}")
    

class RejectInvite(APIView):

    def get(self,request,token):
        invite = GroupInvite.objects.get(token=token)
        if invite.status == "accepted":
            return HttpResponse("Invitation has already been accepted.")
        else:
            invite.status = "rejected"
            invite.save()

            return HttpResponse("Invitation has been rejected successfully.")
    

class GroupInviteView(APIView):

    authentication_classes = [JWTAuthentication]
    def post(self,request,id):

        data = request.data.copy()
        created_invites = []
        errors = []

        emails = data.pop("email",[])

        for email in emails:
            payload = {
                "group": id,
                "invited_by": request.user.id,
                "email":email
            }
        
            serializer =  GroupInviteSerializer(data=payload)
        
            if serializer.is_valid():
                
                serializer.save()
                created_invites.append(serializer.data)
            else:
                errors.append({"emails":email,
                               "errors":serializer.errors})
        if errors:
            return Response({
                "success": False,
                "created": created_invites,
                "errors": errors
            }, status=400)

        return Response({
            "success": True,
            "data": created_invites,
            "message": "Group invitations created successfully."
        })
            
        
        
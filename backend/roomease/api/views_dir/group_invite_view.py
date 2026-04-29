from ..models import Group,GroupInvite,GroupMember,CustomUser
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers_dir.group_invite_serializer import GroupInviteSerializer
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.authentication import JWTAuthentication


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
            <a href="{reject_link}" 
            style="padding:10px 20px;background-color:red;color:white;text-decoration:none;border-radius:5px;">
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

    renderer_classes = [JSONRenderer]
    def get(self,request,token):
        invite = GroupInvite.objects.get(token=token)
        
        user = CustomUser.objects.filter(email = invite.email).first()
        if not user:
            return HttpResponseRedirect("http://127.0.0.1:5501/RoomEase/frontend/html/register.html?email={invite.email}")
        GroupMember.objects.create(user=user,group=invite.group,role="member")
        print("user ho haii",user)
        invite.status = "accepted"
        invite.save()
        

        return Response({"success":True})
    

class RejectInvite(APIView):
    renderer_classes = [JSONRenderer]

    def get(self,request,token):
        invite = GroupInvite.objects.get(token=token)
        invite.status = "rejected"

        invite.save()

        return Response({"success":True})
    

class GroupInviteView(APIView):

    authentication_classes = [JWTAuthentication]
    def post(self,request,id):

        data = request.data.copy()
        
        data["group"] = id
        data["invited_by"] = request.user.id

        serializer =  GroupInviteSerializer(data=data)
        
        if serializer.is_valid():
            
            serializer.save()

            return Response({"success":True,"data":serializer.data,"message":"GroupInvitation Created Successfully."})
        return Response({"success":False,"message":"Something's wrong","errors":serializer.errors})
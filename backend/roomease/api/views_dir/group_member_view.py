from rest_framework.response import Response
from ..models import GroupMember,Group
from rest_framework.views import APIView
from ..serializers_dir.group_member_serializer import GroupMemberSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class GroupMemberView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request,id=False):
        if id:
            group = Group.objects.filter(id=id,is_deleted= False).first()
            member = GroupMember.objects.get(group=group,is_deleted = False)
            serializer = GroupMemberSerializer(member)
            
        members = GroupMember.objects.filter(is_deleted = False)
        serializer = GroupMemberSerializer(members,many=True)

        return Response({"success":True,"data":serializer.data})
    
    def delete(self,request,id):
        user = request.user
       
        member = GroupMember.objects.get(group_id = id,user = user,is_deleted= False)
        member.is_deleted = True
        member.save()
        return Response({"success":True,"message":"Group deleted successfully!"})
        



    
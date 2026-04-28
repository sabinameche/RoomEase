from rest_framework.response import Response
from ..models import GroupMember,Group
from rest_framework.views import APIView
from ..serializers_dir.group_member_serializer import GroupMemberSerializer

class GroupMemberView(APIView):

    def get(self,request,id=False):
        if id:
            group = Group.objects.filter(id=id,is_deleted= False).first()
            member = GroupMember.objects.get(group=group,is_deleted = False)
            serializer = GroupMemberSerializer(member)
            
        members = GroupMember.objects.filter(is_deleted = False)
        serializer = GroupMemberSerializer(members,many=True)

        return Response({"success":True,"data":serializer.data})
    
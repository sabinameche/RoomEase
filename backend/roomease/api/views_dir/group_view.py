from ..serializers_dir.group_serializer import GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Group,GroupMember,GroupInvite
from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class GroupView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=False):
        user = request.user
        
        if id:
            group = Group.objects.filter(id=id,is_deleted= False).first()
            member = GroupMember.objects.get(user = user,group = group, is_deleted = False)
            roles = member.role

            serializer = GroupSerializer(group)
            return Response({"success":True,"data":serializer.data,"role":roles})
        else:
            group = Group.objects.prefetch_related('members').filter(
                    is_deleted=False,
                    members__user=request.user,
                    members__is_deleted = False
                ).distinct()
            serializer = GroupSerializer(group,many=True)

        
        return Response({"success":True,"data":serializer.data})
    
    @transaction.atomic
    def post(self,request):
        group_name = request.data.get("name", "").strip()
        existing_group = Group.objects.filter(name__iexact =group_name).first()

        if existing_group:
            return Response(
                {
                    "success": False,
                    "message": f"Group '{group_name}' already exists."
                })
        data = request.data.copy()
        emails = data.pop("email",[])
        
        data["created_by"] = request.user.id

        serializer = GroupSerializer(data= data)
        
        if serializer.is_valid():
            
            group = serializer.save()
           
            GroupMember.objects.create(user=request.user,group=group,role="ADMIN")
            if emails:
                for email in emails:
                    GroupInvite.objects.create(email=email,group = group,invited_by = request.user)

            return Response({"success":True,"data":serializer.data})
        print(serializer.errors)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
    
    @transaction.atomic
    def patch(self,request,id):
        
        group = Group.objects.get(id = id)
        data = request.data.copy()

        if request.user == group.created_by:
            serializer = GroupSerializer(group,data=data,partial= True)

            if serializer.is_valid():
                serializer.save()

                return Response({"success":True,"data":serializer.data,"message":"Group updated successfully!"})
            
            return Response({"success":False,"message":serializer.errors})
        return Response({"success":False,"message":"You are not allowed to edit!"})
    

    def delete(self,request,id):
        group = Group.objects.get(id=id)
        if request.user == group.created_by:
            group.is_deleted = True
            group.save()

            return Response({"success":True,"message":"Group deleted successfully!"})
        return Response({"success":False,"message":"You are not allowed to delete!"})
        

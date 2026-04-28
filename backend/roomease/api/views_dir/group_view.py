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
        else:
            group = Group.objects.filter(created_by = user,is_deleted = False)

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
        email = data.pop("email")
        
        data["created_by"] = request.user.id

        serializer = GroupSerializer(data= data)
        
        if serializer.is_valid():
            print("why no save??")
            
            serializer.save()
            
            group = Group.objects.get(id=serializer.data["id"])
           
            GroupMember.objects.create(user=request.user,group=group,role="ADMIN")
            GroupInvite.objects.create(email=email,group = group,invited_by = request.user)

            return Response({"success":True,"data":serializer.data})
        print(serializer.errors)
        return Response({"success":False})
    
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
        

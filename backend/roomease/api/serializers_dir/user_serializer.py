from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username','password','email']

        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self,validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        
        user = get_user_model()
        new_user = user.objects.create_user(username=username,password=password,email=email)

        return new_user


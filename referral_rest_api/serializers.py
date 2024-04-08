from rest_framework import serializers


from django.contrib.auth.models import User


from referral_rest_api.models import UserInfo

class UserSeriliazer(serializers.ModelSerializer):
    id=serializers
    class Meta:
        model=User
        fields=['email','password']

        read_only_fields=['id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserInfo
        fields=['name']
        read_only_fields=['referral_id','user']


class UserReferralSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['email','date_joined']


class ReferralSerializer(serializers.ModelSerializer):
    user=UserReferralSerializer(read_only=True)
    class Meta:
        model=UserInfo
        fields=['name','user']
        

        
        

        


from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions,authentication,pagination


from referral_rest_api.serializers import UserSeriliazer,UserInfoSerializer,ReferralSerializer
from referral_rest_api.models import UserInfo
# Create your views here.

class RegisterView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSeriliazer(data=request.data)
        email=request.data.get('email')
        serializer2=UserInfoSerializer(data=request.data)


        #creating users in User Model
        if serializer.is_valid():
            serializer.save(username=email) #username is stored as email

            
            if serializer2.is_valid():

                #referal code block starts here
                if request.data.get('referral_user'):
                    id=request.data.get('referral_user') #id of refered user if passed through front-end
                    referrerd_user=User.objects.get(id=id)  #taking the referred user from DB
                    all_user=User.objects.all() 
                    if referrerd_user in all_user:
                        print(request.data)
                       
                        user=User.objects.get(email=email)
                        id=str(id)
                        serializer2.save(user=user,referral_id=id)  #due to some techinal issue referral_user field
                        # in UserInfo table cannot be called, referral_id field is called instead

                        #giving points to the refered user in UserInfo table using related_name
                        referrerd_user.user_table.points+=10
                        referrerd_user.user_table.save() #save to db

                #user who joins without referal id
                else:
                    user=User.objects.get(email=email)
                    serializer2.save(user=user)
                
                return Response(data={'success_message':'You have successfully created an account','Your unique user id':serializer.instance.id})

        else:
            return Response(data=serializer.errors)



class UserDetailView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        user_data=User.objects.get(username=request.user)
        deserialized_user_data=UserSeriliazer(user_data)
        userinfo_data=UserInfo.objects.get(user=user_data)
        deserialized_userinfo_data=UserInfoSerializer(userinfo_data)
        name=deserialized_userinfo_data.instance.name
        email=deserialized_user_data.instance.email
        referral_code=deserialized_userinfo_data.instance.referral_id
        date=deserialized_user_data.instance.date_joined

        data={'name':name,'email':email,'referral_code':referral_code,' timestamp of registration':date}

        return Response(data)

class SetPagination(pagination.PageNumberPagination):
    #setting 20 users per page
    page_size=20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 2



class UserReferralsView(GenericAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    pagination_class=SetPagination
    def get(self,request,*args,**kwargs):
        
        current_user_referrals=UserInfo.objects.filter(referral_id=request.user)
        #pagination
        page=self.paginate_queryset(current_user_referrals)
        if page is not None:
            deserialize_referrals=ReferralSerializer(page,many=True)
            return self.get_paginated_response(deserialize_referrals.data)

        deserialize_referrals=ReferralSerializer(current_user_referrals,many=True)

        return Response(deserialize_referrals.data)


       
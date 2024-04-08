from django.urls import path,include

from rest_framework.authtoken.views import ObtainAuthToken

from referral_rest_api import views
urlpatterns = [

    path('register/',views.RegisterView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
    path('user/details/',views.UserDetailView.as_view()),
    path('user/referrals/',views.UserReferralsView.as_view()),
    ]
from django.urls import path, include
from .views import AccountLoginView
#AccountLogoutView, AccountDetailsView, OtpVerifyAccountView, CheckIsVerifiedView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('login/', AccountLoginView.as_view()),
    #path('logout/', AccountLogoutView.as_view()),
    #path('userDetail/', AccountDetailsView.as_view()),
    #path('verifyOtp/', OtpVerifyAccountView.as_view()),
    #path('verifyToken/', TokenVerifyView.as_view()),

    # Check For isVerfied View
    #path('isVerified/', CheckIsVerifiedView.as_view()),

    # Friend's Api's
]

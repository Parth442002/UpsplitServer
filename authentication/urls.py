from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('login/', views.AccountLoginView.as_view()),
    path('logout/', views.AccountLogoutView.as_view()),
    path('profile/', views.AccountProfileView.as_view()),

    #path('userDetail/', AccountDetailsView.as_view()),
    #path('verifyOtp/', OtpVerifyAccountView.as_view()),
    #path('verifyToken/', TokenVerifyView.as_view()),

    # Check For isVerfied View
    #path('isVerified/', CheckIsVerifiedView.as_view()),

    # Friend's Api's
]

from django.urls  import path
from users.views  import (SignInView, AdminSigninView ,ChangePasswordView, CheckPasswordView,
                          CheckInformationView, KakaoSigninView, UserLikeView, UserLikeCampaignView)

urlpatterns = [
    path('/signin', SignInView.as_view()),
    path('/admin', AdminSigninView.as_view()),
    path('/password', ChangePasswordView.as_view()),
    path('/checkpassword', CheckPasswordView.as_view()),
    path('/info', CheckInformationView.as_view()),
    path('/signin/kakao', KakaoSigninView.as_view()),
    path('/like/<int:campaign_id>', UserLikeView.as_view()),
    path('/likecampaign', UserLikeCampaignView.as_view())
]

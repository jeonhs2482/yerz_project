from django.urls  import path
from users.views  import SignInView, AdminSigninView ,ChangePasswordView, CheckPasswordView, CheckInformationView, KakaoSigninView

urlpatterns = [
    path('/signin', SignInView.as_view()),
    path('/admin', AdminSigninView.as_view()),
    path('/password', ChangePasswordView.as_view()),
    path('/checkpassword', CheckPasswordView.as_view()),
    path('/info', CheckInformationView.as_view()),
    path('/signin/kakao', KakaoSigninView.as_view()),
]

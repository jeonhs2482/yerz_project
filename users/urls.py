from django.urls  import path
from users.views  import SignInView, AdminSigninView ,ChangePasswordView, CheckPasswordView, CheckInformationView

urlpatterns = [
    path('/signin', SignInView.as_view()),
    path('/admin', AdminSigninView.as_view()),
    path('/password', ChangePasswordView.as_view()),
    path('/checkpassword', CheckPasswordView.as_view()),
    path('/info', CheckInformationView.as_view())
]

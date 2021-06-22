import json, time, jwt

from django.http             import JsonResponse

from rest_framework.views    import APIView
from drf_yasg                import openapi
from drf_yasg.utils          import swagger_auto_schema 

from .models                 import User
from yerz.settings           import SECRET_KEY, JWT_ALGORITHM, JWT_DURATION_SEC
from utils.decorators        import authorization_decorator
from users.serializers       import UserBodySerializer
from .serializers            import PasswordChangeSerializer

class SignInView(APIView):
    @swagger_auto_schema(request_body=UserBodySerializer)
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if user.password != password:
                return JsonResponse({"status": "UNAUTHORIZATION"}, status=401)

            new_token = jwt.encode(
                                    {
                                        'user_id': user.id,
                                        'iat'    : int(time.time()),
                                        'exp'    : int(time.time()) + JWT_DURATION_SEC
                                    }, 
                                    SECRET_KEY, 
                                    JWT_ALGORITHM
                                  )

            return JsonResponse({"status": "SUCCESS", "data": {"token": new_token}}, status=200)

        except KeyError: 
            return JsonResponse({"status": "KEY_ERROR", "message": 'Key_Error'}, status=400)
        
        except User.DoesNotExist: 
            return JsonResponse({"status": "INVALID_USER"}, status=401)
        
class ChangePasswordView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)], 
        request_body=PasswordChangeSerializer)
    @authorization_decorator
    def post(self, request):
        data         = json.loads(request.body)
        user         = request.user
        new_password = data['password']
        
        user.password = new_password
        user.save()

        return JsonResponse({"message": "SUCCESS"}, status=200)


        
        




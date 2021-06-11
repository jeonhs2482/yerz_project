import jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import JWT_SECRET_KEY, JWT_ALGORITHM

def authorization_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    =   request.headers.get('Authorization', None)
            payload         =   jwt.decode(access_token, JWT_SECRET_KEY ,algorithm= JWT_ALGORITHM)
            login_user      =   User.objects.get(id=payload['user_id'])
            request.user    =   login_user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'},status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'},status=400)

        return func(self, request, *args, **kwargs)

    return wrapper

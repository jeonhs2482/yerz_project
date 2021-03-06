import jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import JWT_ALGORITHM, SECRET_KEY

def authorization_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        access_token    =   request.headers.get('Authorization', None)
        try:
            payload         =   jwt.decode(access_token.encode('utf-8'), SECRET_KEY , JWT_ALGORITHM)
            login_user      =   User.objects.get(id=payload['user_id'])
            request.user    =   login_user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'status': 'INVALID_TOKEN'},status=400)

        except User.DoesNotExist:
            return JsonResponse({'status': 'INVALID_USER'},status=400)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'status': 'EXPIRED_TOKEN'},status=400)

    return wrapper

def chekuser_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        access_token    =   request.headers.get('Authorization', None)
        try:
            if access_token:
                payload         =   jwt.decode(access_token.encode('utf-8'), SECRET_KEY , JWT_ALGORITHM)
                login_user      =   User.objects.get(id=payload['user_id'])
                request.user    =   login_user
                return func(self, request, *args, **kwargs)

            else:
                request.user = None
                return func(self, request, *args, **kwargs)
            
        except:
            request.user = None
            return func(self, request, *args, **kwargs)
    
    return wrapper


import json, time, jwt, requests

from django.http             import JsonResponse

from rest_framework.views    import APIView
from drf_yasg                import openapi
from drf_yasg.utils          import swagger_auto_schema 

from .models                 import User, Like
from campaigns.models        import Campaign
from yerz.settings           import SECRET_KEY, JWT_ALGORITHM, JWT_DURATION_SEC
from utils.decorators        import authorization_decorator
from users.serializers       import UserBodySerializer
from .serializers            import PasswordChangeSerializer

class SignInView(APIView):  #일반로그인
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

class AdminSigninView(APIView):  #어드민 계정 로그인
    @swagger_auto_schema(request_body=UserBodySerializer)
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if user.password != password:
                return JsonResponse({"status": "UNAUTHORIZATION"}, status=401)

            if user.admin == 0:
                return JsonResponse({"status": "NOT_ADMIN"}, status=401)

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

class ChangePasswordView(APIView):  #비밀번호 변경
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

        return JsonResponse({"status": "SUCCESS"}, status=200)

class CheckPasswordView(APIView):  #현재 비밀번호 확인
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)], 
        request_body=PasswordChangeSerializer)
    @authorization_decorator
    def post(self, request):
        data     = json.loads(request.body)
        user     = request.user
        password = data['currentpassword']

        if user.password == password:
            return JsonResponse({"status": "SUCCESS"}, status=200)
        else:
            return JsonResponse({"status": "INCORRECT_PASSWORD"}, status=401)

class CheckInformationView(APIView):  #로그인한 유저 정보 확인
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)])
    @authorization_decorator
    def get(self, request):
        user = request.user
        if user.kakao_email:
            user_info = {
                'email'       : user.kakao_email,
                'name'        : user.name,
                'phone_number': user.phone_number
            }
        else:
            user_info = {
                'email'       : user.email,
                'name'        : user.name,
                'phone_number': user.phone_number
            }

        return JsonResponse({"status": "SUCCESS", "data": user_info}, status=200)

class KakaoSigninView(APIView):  #카카오 소셜로그인
    def post(self, request):
        try:
            data         = json.loads(request.body)
            access_token = data['access_token']
            response     = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
            data         = response.json()
            
            if response.status_code != 200:
                    return JsonResponse({"status": "API_ERROR", "message": data['msg']}, status=response.status_code)

            username           = data['kakao_account']['profile']['nickname']
            email              = data['kakao_account']['email']

            if (User.objects.filter(kakao_email = email).exists()):
                user = User.objects.get(kakao_email = email)

            else:
                user = User.objects.create(
                                            name          = username,
                                            kakao_email   = email,
                                        )
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

        except KeyError as e:
            return JsonResponse({"status": "KEY_ERROR", "message": f'Key Error in Field "{e.args[0]}"'}, status=400)

        except requests.exceptions.Timeout as e:
            return JsonResponse({"status": "TIMEOUT_ERROR", "message": e.response.message}, status=e.response.status_code)

        except requests.exceptions.ConnectionError as e:
            return JsonResponse({"status": "CONNECTION_ERROR", "message": e.response.message}, status=e.response.status_code)

        except requests.exceptions.HTTPError as e:
            return JsonResponse({"status": "TIMEOUT_ERROR", "message": e.response.message}, status=e.response.status_code)

class UserLikeView(APIView):  #유저 좋아요 데이터
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)])
    @authorization_decorator
    def patch(self, request, campaign_id):
        try:
            user     = request.user
            like     = Like.objects.filter(user_id=user.id, campaign_id=campaign_id)

            if like:
               liked = like[0]
               campaign = liked.campaign
               campaign.is_liked = False
               campaign.save()
               like.delete()

               return JsonResponse({"status": "SUCCESS", "is_liked": campaign.is_liked}, status=200)

            else:
                like = Like.objects.create(user_id=user.id, campaign_id=campaign_id)
                campaign = like.campaign
                campaign.is_liked = True
                campaign.save()
                
                return JsonResponse({"status": "SUCCESS", "is_liked": campaign.is_liked}, status=200) 

        except Campaign.DoesNotExist:
            return JsonResponse({"status": "CAMPAIGN_NOT_FOUND", "message": "존재하지 않는 캠페인입니다."}, status=404)

class UserLikeCampaignView(APIView):  #유저가 좋아요한 캠페인 확인
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)])
    @authorization_decorator
    def get(self, request):
        user           = request.user
        liked_campaign = Like.objects.filter(user_id=user.id)

        campaign      = [{
            'id'       : campaigns.campaign.id,
            'url'      : campaigns.campaign.image,
            'subtitle' : {
                'brand'   : campaigns.campaign.brand,
                'host': campaigns.campaign.host
            },
            'title'    : campaigns.campaign.title,
            'is_liked' : user in campaigns.campaign.user_campaign.all()
        } for campaigns in liked_campaign]

        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)
                
          
                

            


        
                                        
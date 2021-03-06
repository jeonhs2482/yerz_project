import json

from django.http           import JsonResponse
from django.utils          import timezone

from drf_yasg              import openapi
from drf_yasg.utils        import swagger_auto_schema
from rest_framework.views  import APIView

from utils.decorators      import authorization_decorator, chekuser_decorator
from users.models          import PaymentOption, Payment, Like
from campaigns.models      import Campaign, Option
from .serializers          import PaymentRegisterSerializer

class CampaignListView(APIView):  #로그인한 유저가 참여한 캠페인리스트
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request):
        user          = request.user
        user_payment  = Payment.objects.filter(user_id=user.id).order_by('-created_at')
        campaign      = [{
            'id'       : payments.id,
            'url'      : payments.option.campaign.image,
            'subtitle' : {
                'brand' : payments.option.campaign.brand,
                'host'  : payments.option.campaign.host
            },
            'title'    : payments.option.campaign.title,
            'is_liked' : user in payments.option.campaign.user_campaign.all()
        } for payments in user_payment]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)

class AllCampaignListView(APIView):  #메인페이지 전체 캠페인리스트  
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @chekuser_decorator
    def get(self,request):
        user          = request.user
        all_campaign  = Campaign.objects.all()
        campaign      = [{
            'id'       : campaigns.id,
            'url'      : campaigns.image,
            'subtitle' : {
                'brand'   : campaigns.brand,
                'host': campaigns.host
            },
            'title'    : campaigns.title,
            'is_liked' : user in campaigns.user_campaign.all()
        } for campaigns in all_campaign]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)

class CampaignDetailView(APIView):  #캠페인 상세정보페이지
    def get(self, request, campaign_id):
        try:
            campaign        = Campaign.objects.get(id=campaign_id)
            campaign_option = Option.objects.filter(campaign_id=campaign_id)
            detail_info = {
                'result'   : {
                    'id'   : campaign.id,
                    'title': campaign.title,
                    'subtitle' : {
                        'brand': campaign.brand,
                        'host' : campaign.host
                    },
                    'url': campaign.image,
                    'option' : [{
                        'option_id': option.id,
                        'title'    : option.title,
                        'price'    : option.price,
                        'quantity' : 0,
                        'stock'    : 10
                    } for option in campaign_option]
                }
            }
            return JsonResponse({'status': "SUCCESS", 'data': {'campaign':detail_info}}, status=200)
        except Campaign.DoesNotExist:
            return JsonResponse({"status": "CAMPAIGN_NOT_FOUND", "message": "존재하지 않는 캠페인입니다."}, status=404)
        except KeyError: 
            return JsonResponse({"status": "KEY_ERROR", "message": 'KEY_ERROR'}, status=400)

class UserCampaignDetailView(APIView):  #유저가 참여한 캠페인 주문정보페이지
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request, payment_id):
        try:
            user            = request.user
            payment         = Payment.objects.get(id=payment_id)
            payment_options = PaymentOption.objects.filter(payment_id=payment_id)
            option_list     = []
            for payment_option in payment_options:
                option_list.append(payment_option)
            detail_info  = {
                'id': payment.id,
                'more': [
                    {
                        'title': "캠페인 참여정보",
                        'detail': {
                            'campname': payment.option.campaign.title,
                            'username': user.name,
                            'date'    : payment.created_at.strftime("%Y.%m.%d"),
                            'option'  : [{
                                'title'   : options.title,
                                'quantity': options.quantity
                            }for options in option_list]                                      
                        }
                    },
                    {
                        'title' : "결제 정보",
                        'detail': {
                            'payment': payment.payment_type,
                            'price'  : payment.total
                        }
                    },
                    {
                        'title' : "배송 정보",
                        'detail': {
                            'recipient': payment.name,
                            'contact'  : payment.phone_number,
                            'address'  : payment.address,
                            'request'  : payment.delivery_request
                        }
                    }
                ]
            }
            return JsonResponse({'status': "SUCCESS", 'data': {'campaign':detail_info}}, status=200)
        except Campaign.DoesNotExist:
            return JsonResponse({"status": "PAYMENT_NOT_FOUND", "message": "존재하지 않는 주문입니다."}, status=404)
        except KeyError: 
            return JsonResponse({"status": "KEY_ERROR", "message": 'KEY_ERROR'}, status=400)

class PaymentRegisterView(APIView):  #주문정보 입력페이지
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)], 
        request_body=PaymentRegisterSerializer)
    @authorization_decorator
    def post(self, request):
        user     = request.user
        data     = json.loads(request.body)
        option   = Option.objects.get(id=data['option'][0]['option_id'])
        payment  = Payment.objects.create(
            orderer_name     = data['orderer'],
            orderer_contact  = data['orderer_contact'],
            name             = data['recipient'],
            phone_number     = data['recipient_contact'],
            address          = data['address'],
            payment_type     = data['payment'],
            delivery_request = data['request'],
            total            = data['total'],
            user_id          = user.id,
            option_id        = option.id
        )

        for option in data['option']:
            PaymentOption.objects.create(
                title      = option['title'],
                price      = option['price'],
                quantity   = option['quantity'],
                payment_id = payment.id
            )
        return JsonResponse({"status": "SUCCESS"}, status=200)

class AdminCampaignListView(APIView):  #어드민 계정 로그인시 캠페인리스트 
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request):
        user          = request.user
        user_campaign = Campaign.objects.filter(user_id=user.id)
        campaign      = [{
            'id'       : campaign.id,
            'url'      : campaign.image,
            'subtitle' : {
                'brand': campaign.brand,
                'host' : campaign.host
            },
            'title'    : campaign.title,
            'is_liked' : user in campaign.user_campaign.all()
        } for campaign in user_campaign]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)

class AdminCampaignDetailView(APIView):  #어드민 계정 로그인시 캠페인 상세정보페이지
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request, campaign_id):
        try:
            admin_payment   = Payment.objects.filter(option__campaign_id=campaign_id).order_by('-created_at')
            
            detail_info  = [
                {
                'id': payment.id,
                'info': {
                    'orderer'          : payment.orderer_name,
                    'orderer_contact'  : payment.orderer_contact,
                    'recipient'        : payment.name,
                    'recipient_contact': payment.phone_number,
                    'address'          : payment.address,
                    'option'           : [{
                            'title'    : payment.title,
                            'quantity' : payment.quantity
                        }for payment in payment.payment_option.all()],
                    'payment'          : payment.payment_type,
                    'price'            : payment.total,
                    'date'             : payment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'status'           : '결제완료' if payment.payment_type == '카드' else '입금대기중'
                }
            }
                for payment in admin_payment]
            return JsonResponse({'status': "SUCCESS", 'data': {'campaign':detail_info}}, status=200)
        except Campaign.DoesNotExist:
            return JsonResponse({"status": "CAMPAIGN_NOT_FOUND", "message": "존재하지 않는 캠페인입니다."}, status=404)
        except KeyError: 
            return JsonResponse({"status": "KEY_ERROR", "message": 'Key_Error'}, status=400)

class AllMontlySalesView(APIView):  #어드민 계정 로그인시 캠페인별 최근 3개월 판매량
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request):
        user          = request.user
        user_campaign = Campaign.objects.filter(user_id=user.id)
        current_time  = int(timezone.now().strftime('%m'))
            
        result = [
            {
                'id'  : campaign.id,
                'name': campaign.brand,
                'data': {
                    'twoMonthsAgo': sum([num.quantity for num in PaymentOption.objects.filter(payment__option__campaign_id=campaign.id, payment__created_at__month=current_time-2)]),
                    'last'        : sum([num.quantity for num in PaymentOption.objects.filter(payment__option__campaign_id=campaign.id, payment__created_at__month=current_time-1)]),
                    'current'     : sum([num.quantity for num in PaymentOption.objects.filter(payment__option__campaign_id=campaign.id, payment__created_at__month=current_time)])
                }
            }
        for campaign in user_campaign]

        return JsonResponse({'status': "SUCCESS", 'data': {'result':result}}, status=200)

class MontlySalesView(APIView):  #어드민 계정 로그인시 옵션별 최근 3개월 판매량
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request, campaign_id):
        campaign     = Campaign.objects.get(id=campaign_id)
        options      = Option.objects.filter(campaign__id=campaign.id)
        current_time = int(timezone.now().strftime('%m'))

        result = [
            {
                'id'  : option.id,
                'name': option.title,
                'data': {
                    'twoMonthsAgo': sum([num.quantity for num in PaymentOption.objects.filter(title=option.title, payment__created_at__month=current_time-2)]),
                    'last'        : sum([num.quantity for num in PaymentOption.objects.filter(title=option.title, payment__created_at__month=current_time-1)]),
                    'current'     : sum([num.quantity for num in PaymentOption.objects.filter(title=option.title, payment__created_at__month=current_time)])
                }
            }
        for option in options]
        return JsonResponse({'status': "SUCCESS", 'data': {'result':result}}, status=200)

class CampaignTotalView(APIView):  #캠페인 총 판매금액 및 주문자 수 정보
    def get(self, request, campaign_id):
        campaign      = Campaign.objects.get(id=campaign_id)
        total_payment = Payment.objects.filter(option__campaign__id=campaign_id)

        result = {
            'id'         : campaign.id,
            'total_price': sum([payment.total for payment in total_payment]),
            'total_num'  : total_payment.count() 
        }
        return JsonResponse({'status': "SUCCESS", 'data': {'result':result}}, status=200)  
        



    
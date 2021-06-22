import json

from django.http           import JsonResponse

from drf_yasg              import openapi
from drf_yasg.utils        import swagger_auto_schema
from rest_framework.views  import APIView

from utils.decorators      import authorization_decorator
from users.models          import PaymentOption, Payment
from campaigns.models      import Campaign, Option
from .serializers          import PaymentRegisterSerializer

class CampaignListView(APIView):
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
                'brand' : payments.option.campaign.subtitle.brand,
                'host'  : payments.option.campaign.subtitle.host
            },
            'title'    : payments.option.campaign.title
        } for payments in user_payment]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)

class AllCampaignListView(APIView):
    def get(self,request):
        all_campaign  = Campaign.objects.all()
        campaign      = [{
            'id'       : campaigns.id,
            'url'      : campaigns.image,
            'subtitle' : {
                'brand'   : campaigns.subtitle.brand,
                'host': campaigns.subtitle.host
            },
            'title'    : campaigns.title
        } for campaigns in all_campaign]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)

class CampaignDetailView(APIView):
    def get(self, request, campaign_id):
        try:
            campaign        = Campaign.objects.get(id=campaign_id)
            campaign_option = Option.objects.filter(campaign_id=campaign_id)
            detail_info = {
                'result'   : {
                    'id'   : campaign.id,
                    'title': campaign.title,
                    'subtitle' : {
                        'brand': campaign.subtitle.brand,
                        'host' : campaign.subtitle.host
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

class UserCampaignDetailView(APIView):
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
            all_price    = [options.price for options in option_list]
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
                            'price'  : float(sum(all_price))
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
        
class PaymentRegisterView(APIView):
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
        return JsonResponse({"message": "SUCCESS"}, status=200)
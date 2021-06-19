import json

from django.http           import JsonResponse

from drf_yasg              import openapi
from drf_yasg.utils        import swagger_auto_schema
from rest_framework.views  import APIView

from utils.decorators      import authorization_decorator
from users.models          import UserOption, Payment
from campaigns.models      import Campaign, Option

class CampaignListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request):
        user          = request.user
        user_payment  = Payment.objects.filter(user_id=user.id)
        campaign      = [{
            'id'       : payments.campaign.id,
            'url'      : [payments.campaign.image, payments.campaign.image, payments.campaign.image],
            'subtitle' : {
                'brand'   : payments.campaign.subtitle.brand,
                'hostname': payments.campaign.subtitle.host
            },
            'title'    : payments.campaign.title
        } for payments in user_payment]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)

class AllCampaignListView(APIView):
    def get(self,request):
        all_campaign  = Campaign.objects.all()
        campaign      = [{
            'id'       : campaigns.id,
            'url'      : [campaigns.image, campaigns.image, campaigns.image],
            'subtitle' : {
                'brand'   : campaigns.subtitle.brand,
                'hostname': campaigns.subtitle.host
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
                    'url': [
                        campaign.image, campaign.image, campaign.image 
                    ],
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
    def get(self, request, campaign_id):
        try:
            user         = request.user
            campaign     = Campaign.objects.get(id=campaign_id)
            user_options = UserOption.objects.filter(user_id=user.id, option__campaign_id=campaign_id)
            user_payment = Payment.objects.filter(user_id=user.id, campaign_id=campaign_id)
            option_list  = []
            for user_option in user_options:
                option_list.append(user_option)
            all_price    = [options.price for options in option_list]
            detail_info  = {
                'id': campaign.id,
                'more': [
                    {
                        'title': "캠페인 참여정보",
                        'detail': {
                            'campname': campaign.title,
                            'username': user.name,
                            'date'    : user_payment.first().created_at.strftime("%Y.%m.%d"),
                            'option'  : [{
                                'title'   : options.title,
                                'quantity': options.quantity
                            } for options in option_list]
                        }
                    },
                    {
                        'title' : "결제 정보",
                        'detail': {
                            'payment': user_payment.first().payment_type,
                            'price'  : float(sum(all_price))
                        }
                    },
                    {
                        'title' : "배송 정보",
                        'detail': {
                            'recipient': user_payment.first().name,
                            'contact'  : user_payment.first().phone_number,
                            'address'  : user_payment.first().address,
                            'request'  : user_payment.first().delivery_request
                        }
                    }
                ]
            }
            return JsonResponse({'status': "SUCCESS", 'data': {'campaign':detail_info}}, status=200)
        except Campaign.DoesNotExist:
            return JsonResponse({"status": "CAMPAIGN_NOT_FOUND", "message": "존재하지 않는 캠페인입니다."}, status=404)
        
class PaymentRegisterView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def post(self, request):
        user     = request.user
        data     = json.loads(request.body)
        option   = Option.objects.get(id=data['option'][0]['option_id'])
        campaign = option.campaign
        Payment.objects.create(
            orderer_name     = data['orderer'],
            orderer_contact  = data['orderer_contact'],
            name             = data['recipient'],
            phone_number     = data['recipient_contact'],
            address          = data['address'],
            payment_type     = data['payment'],
            delivery_request = data['request'],
            user_id          = user.id,
            campaign_id      = campaign.id
        )

        for option in data['option']:
            UserOption.objects.create(
                title     = option['title'],
                price     = option['price'],
                quantity  = option['quantity'],
                user_id   = user.id,
                option_id = option['option_id']
            )
        return JsonResponse({"message": "SUCCESS"}, status=200)
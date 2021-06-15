import json

from django.views          import View
from django.http           import JsonResponse

from drf_yasg              import openapi
from drf_yasg.utils        import swagger_auto_schema
from rest_framework.views  import APIView

from utils.decorators      import authorization_decorator
from users.models          import UserCampaign, UserOption
from campaigns.models      import Campaign

class CampaignListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request):
        user          = request.user
        user_campaign = UserCampaign.objects.filter(user_id=user.id)
        campaign = [{
            'id'       : campaigns.campaign.id,
            'url'      : [campaigns.campaign.image, campaigns.campaign.image, campaigns.campaign.image],
            'subtitle' : {
                'brand'   : campaigns.campaign.subtitle.brand,
                'hostname': campaigns.campaign.subtitle.host
            },
            'title'    : campaigns.campaign.title
        } for campaigns in user_campaign ]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign}}, status=200)       

class CampaignDetailView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('authorization', openapi.IN_HEADER, description="please enter login token", type=openapi.TYPE_STRING)]
    )
    @authorization_decorator
    def get(self, request, campaign_id):
        try:
            user         = request.user
            campaign     = Campaign.objects.get(id=campaign_id)
            user_options = UserOption.objects.filter(user_id=user.id, option__campaign_id=campaign_id)
            option_list  = []
            for user_option in user_options:
                option_list.append(user_option)
            all_price    = [options.option.price for options in option_list]
            detail_info  = {
                'id': campaign.id,
                'more': [
                    {
                        'title': "캠페인 참여정보",
                        'detail': {
                            'campname': campaign.title,
                            'username': user.name,
                            'date'    : option_list[0].option.payment.created_at.strftime("%Y.%m.%d"),
                            'option'  : [{
                                'title'   : options.option.title,
                                'quantity': options.option.quantity
                            } for options in option_list]
                        }
                    },
                    {
                        'title' : "결제 정보",
                        'detail': {
                            'payment': option_list[0].option.payment.payment_type,
                            'price'  : float(sum(all_price))
                        }
                    },
                    {
                        'title' : "배송 정보",
                        'detail': {
                            'recipient': option_list[0].option.payment.name,
                            'contact'  : option_list[0].option.payment.phone_number,
                            'address'  : option_list[0].option.payment.address,
                            'request'  : option_list[0].option.payment.delivery_request
                        }
                    }
                ]
            }
            return JsonResponse({'status': "SUCCESS", 'data': {'campaign':detail_info}}, status=200)
            
        except Campaign.DoesNotExist:
            return JsonResponse({"status": "CAMPAIGN_NOT_FOUND", "message": "존재하지 않는 캠페인입니다."}, status=404)
        

import json

from django.views          import View
from django.http           import JsonResponse

from utils.decorators      import authorization_decorator
from users.models          import UserCampaign, UserOption
from campaigns.models      import Campaign, Payment

class CampaignListView(View):
    @authorization_decorator
    def get(self, request):
        user          = request.user
        user_campaign = UserCampaign.objects.filter(user_id=user.id)
        campaign_info = [{
            'id'   : campaigns.campaign.id,
            'image': campaigns.campaign.image,
            'host' : campaigns.campaign.subtitle.host,
            'brand': campaigns.campaign.subtitle.brand,
            'title': campaigns.campaign.title
        } for campaigns in user_campaign ]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign_info}}, status=200)       

class CampaignDetailView(View):
    @authorization_decorator
    def get(self, request, campaign_id):
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
        

        

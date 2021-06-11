import json
from users.models import UserCampaign

from django.views          import View
from django.http           import JsonResponse

from utils.decorators      import authorization_decorator
from users.models          import User
class CampaignListView(View):
    #@authorization_decorator
    def get(self, request):
        user          = User.objects.get(id=6)
        user_campaign = UserCampaign.objects.filter(user_id=user.id)
        campaign_info = [{
            'id'   : campaigns.campaign.id,
            'image': campaigns.campaign.image,
            'host' : campaigns.campaign.subtitle.host,
            'brand': campaigns.campaign.subtitle.brand,
            'title': campaigns.campaign.title
        } for campaigns in user_campaign ]
        return JsonResponse({'status': "SUCCESS", 'data': {'campaign':campaign_info}}, status=200)         
        

from django.urls  import path
from campaigns.views  import AllCampaignListView, UserCampaignDetailView, CampaignListView, CampaignDetailView

urlpatterns = [
    path('/userlist', CampaignListView.as_view()),
    path('/userdetail/<int:campaign_id>', UserCampaignDetailView.as_view()),
    path('/list', AllCampaignListView.as_view()),
    path('/detail/<int:campaign_id>', CampaignDetailView.as_view())
]


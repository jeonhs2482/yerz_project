from django.urls  import path
from campaigns.views  import CampaignDetailView, CampaignListView

urlpatterns = [
    path('/list', CampaignListView.as_view()),
    path('/detail/<int:campaign_id>', CampaignDetailView.as_view())
]


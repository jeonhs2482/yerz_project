from django.urls  import path
from campaigns.views  import CampaignListView

urlpatterns = [
    path('/list', CampaignListView.as_view()),
]


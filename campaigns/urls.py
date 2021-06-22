from django.urls  import path
from campaigns.views  import (AllCampaignListView, UserCampaignDetailView, CampaignListView,
                              CampaignDetailView, PaymentRegisterView, AdminCampaignListView, AdminCmapaignDetailView)

urlpatterns = [
    path('/userlist', CampaignListView.as_view()),
    path('/userdetail/<int:payment_id>', UserCampaignDetailView.as_view()),
    path('/list', AllCampaignListView.as_view()),
    path('/detail/<int:campaign_id>', CampaignDetailView.as_view()),
    path('/pay', PaymentRegisterView.as_view()),
    path('/adminlist', AdminCampaignListView.as_view()),
    path('/admindetail/<int:campaign_id>', AdminCmapaignDetailView.as_view())
]


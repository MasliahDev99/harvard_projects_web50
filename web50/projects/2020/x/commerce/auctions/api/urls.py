from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet, BidViewSet,UserBidHistoryView  # Correct import

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)  # Use AuctionViewSet directly
router.register(r'bids', BidViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bids/user/<int:user_id>/', UserBidHistoryView.as_view(), name='user_bid_history'),
]
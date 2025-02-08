from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet, BidViewSet  # Correct import

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)  # Use AuctionViewSet directly
router.register(r'bids', BidViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
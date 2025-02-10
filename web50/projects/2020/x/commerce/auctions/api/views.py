from rest_framework import viewsets,status,generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from ..models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer, BidHistoryUserSerializer

"""
    Porpuse of views.py

    1. AuctionViewSet: This viewset is responsible for handling CRUD operations for the Auction model.
    2. BidViewSet: This viewset is responsible for handling CRUD operations for the Bid model.
    3. UserBidHistoryView: This view is responsible for retrieving the bid history of a specific user.


"""


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    parser_classes = [MultiPartParser, FormParser]


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class UserBidHistoryView(generics.ListAPIView):
    serializer_class = BidHistoryUserSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Bid.objects.filter(user_id=user_id).select_related('auction','auction__category')


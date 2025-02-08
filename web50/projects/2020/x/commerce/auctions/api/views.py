from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from ..models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    parser_classes = [MultiPartParser, FormParser]


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
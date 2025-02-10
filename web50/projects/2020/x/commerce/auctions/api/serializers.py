from rest_framework import serializers
from ..models import Auction, Bid

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = [
            'id', 
            'created_by',
            'title', 
            'description', 
            'starting_bid', 
            'image',
            'end_date', 
            'end_time', 
            'is_active', 
            'winner']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            'id', 
            'auction', 
            'user', 
            'amount', 
            'created_at', 
            'status'
            ]

class BidHistoryUserSerializer(serializers.ModelSerializer):
    auction_title = serializers.CharField(source='auction.title',read_only=True)
    category_name = serializers.CharField(source='auction.category.name',read_only=True)

    class Meta:
        model = Bid
        fields = [
            'id',
            'auction_title',
            'category_name',
            'amount',
            'created_at',
           'status'
        ]

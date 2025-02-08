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
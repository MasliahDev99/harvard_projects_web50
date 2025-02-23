# Specification

Complete the implementation of your auction site. You must fulfill the following requirements:

## Models
Your application should have at least three models in addition to the `User` model:  
- One for auction listings  
- One for bids  
- One for comments made on auction listings  

It's up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.

## Create Listing
Users should be able to visit a page to create a new listing. They should be able to specify:  
- A title for the listing  
- A text-based description  
- The starting bid amount  
- (Optional) A URL for an image for the listing  
- (Optional) A category (e.g., Fashion, Toys, Electronics, Home, etc.)

## Active Listings Page
The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum):  
- The title  
- Description  
- Current price  
- Photo (if one exists for the listing)

## Listing Page
Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.

### Features for Signed-in Users:
- **Watchlist**: Users should be able to add/remove the item from their "Watchlist."
- **Bidding**: Users should be able to place a bid. The bid must be:
  - At least as large as the starting bid
  - Greater than any other bids that have been placed
  - If the bid doesn’t meet these criteria, an error should be displayed.
- **Auction Owner Actions**: If the signed-in user is the one who created the listing, they should have the ability to "close" the auction, making the highest bidder the winner and marking the listing as no longer active.
- **Winning Bid Display**: If a user won a closed listing, the page should indicate that they won the auction.
- **Comments**: Users should be able to add comments to the listing page. The page should display all comments made on the listing.

## Watchlist
Users who are signed in should be able to visit a **Watchlist** page, which should display all listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

## Categories
Users should be able to visit a page that displays a list of all listing categories. Clicking on a category should take the user to a page displaying all active listings in that category.

## Django Admin Interface
Via the Django admin interface, a site administrator should be able to:
- View
- Add
- Edit
- Delete any listings, comments, and bids made on the site.

---

# Problems Faced During Development

## 1. Watchlist Button Not Updating
### 🛑 Problem:
When a user added an auction to their watchlist, the button state was incorrectly showing 'remove' for all users.

### ✅ Solution:
Implemented filtering of auctions by the logged-in user to ensure the button state is accurate.

#### **Backend (utils.py)**
```python
def get_user_watchlist_auctions(user, **kwargs):
    return Auction.objects.filter(
        watchlist__user=user,
        **kwargs,
    ).prefetch_related(
        Prefetch('watchlisted_by', queryset=Watchlist.objects.filter(user=user), to_attr='user_watchlist')
    )
```

#### **Frontend (Django Template)**
```django
{% if auction.user_watchlist %}
    <i class="fas fa-heart me-1"></i> Remove
{% else %}
    <i class="far fa-heart me-1"></i> Watch
{% endif %}
```
#### **Backend (Django View)**
```python
   def get_auctions_by(prefetch_watchlist=False, **kwargs):
    """
    Get auctions based on the provided filters.

    Args:
        prefetch_watchlist (bool): Whether to prefetch related watchlist items.
        **kwargs: Additional keyword arguments for filtering.
    Returns:
        QuerySet: Filtered auctions.
    """
    queryset = Auction.objects.filter(**kwargs)
    
    # Prefetch related watchlist items if needed
    if prefetch_watchlist:
        queryset = queryset.prefetch_related(
            Prefetch('watchlisted_by', queryset=Watchlist.objects.all(), to_attr='user_watchlist')
        )
    
    return queryset
```
## 2. Nested Comments Like a Social Media Thread

### 🛑 Problem:
Implementing nested comments to work similarly to social media threads was challenging. Managing parent-child relationships and rendering them properly in the frontend was tricky.

### ✅ Solution:
Added a **self-referential ForeignKey** in the `Comment` model to allow comments to be replies to other comments.

#### **Updated `Comment` Model**
```python
from django.db import models
from django.conf import settings

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    
    # Self-referential foreign key for nested comments
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
```
### 🔍 Explanation:
- **`parent` Field**: This field is a self-referential ForeignKey. It allows a comment to be a reply to another comment. If a comment is a top-level comment (not a reply), the `parent` field is set to `None`.

- if `parent`  is `null` , it means the comment is a top-level comment.

- if `parent` has a value, it means the comment is a reply to another comment.

- Using `related_name='replies'`, we can access all replies to a comment using `comment.replies.all()`.

This allows comments to be stored as parent-child relationships, making it possible to implement nested replies, just like in a social media thread. 🎯

## 📽️ Video Tutorial

view it directly on [YouTube](https://youtu.be/o__nnPQY4NY).


# API Documentation 📖

### Structure

- **auctions/api/serializers.py**: Defines serializers for auction and bid models, allowing conversion of model instances to JSON and vice versa.
- **auctions/api/views.py**: Contains API views that handle HTTP requests for auctions and bids, using serializers to process data.
- **auctions/api/urls.py**: Defines API routes, mapping URLs to corresponding views.

### Possible Uses

- **Auction Management**: Allows creating, reading, updating, and deleting auctions via HTTP requests, facilitating auction management from external applications or custom user interfaces.
- **Bid Tracking**: Provides a mechanism to track bids made on each auction, allowing users to view bid history and the current state of each auction.

### Planned Use

- **Real-time Updates**: The API will be used to periodically check auctions nearing their end date and update their status accordingly.
- **Winner Determination**: After an auction ends, the API will determine the winner based on the highest bid and update the frontend to display the winner.




## 📩 Contact & Feedback

If you have any suggestions, constructive criticism, or recommendations regarding **best practices**, **code optimization**, or **improvements in project architecture**, I’d love to hear them.  

You can reach me through the following channels:  

📧 **Email:** [felipe_dev99@outlook.es](felipe_dev99@outlook.es)  
🐙 **GitHub:** [https://github.com/MasliahDev99](https://github.com/MasliahDev99)  
 

All feedback is welcome to help improve and learn. Thanks for your time! 🚀

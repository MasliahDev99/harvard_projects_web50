from . import utils

def watchlist_count(request):
    if request.user.is_authenticated:
        user = request.user
        watchlist_count = len(utils.get_watchlist(user))
    else:
        watchlist_count = 0
    return {'watchlist_count': watchlist_count}
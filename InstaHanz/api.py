from InstaHanz.backends.instaloader_backend import (
    fetch_profile_instaloader,
    fetch_posts_instaloader,
    fetch_followers_instaloader,
    download_profile_picture,
    analyze_bio_text,
    calculate_engagement_rate,
    search_hashtag_posts,
    search_location_posts,
)
from InstaHanz.backends.ai_analysis import predict_account_type

def get_user_info(username, backend_user=None):
    return fetch_profile_instaloader(username, login_user=backend_user)

def get_user_posts_summary(username, backend_user=None, limit=5):
    return fetch_posts_instaloader(username, limit=limit, login_user=backend_user)

def get_user_followers(username, backend_user=None, limit=20):
    return fetch_followers_instaloader(username, login_user=backend_user, limit=limit)

def download_pfp(username, backend_user=None):
    return download_profile_picture(username, login_user=backend_user)

def get_bio_analysis(bio):
    return analyze_bio_text(bio)

def get_engagement_analysis(posts, followers):
    return calculate_engagement_rate(posts, followers)

def get_hashtag_posts(hashtag, backend_user=None, limit=10):
    return search_hashtag_posts(hashtag, login_user=backend_user, limit=limit)

def get_location_posts(location, backend_user=None, limit=10):
    return search_location_posts(location, login_user=backend_user, limit=limit)

def get_account_prediction(profile_info, engagement_analysis=None):
    return predict_account_type(profile_info, engagement_analysis)

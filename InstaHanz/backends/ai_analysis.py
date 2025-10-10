def predict_account_type(profile_info, engagement_analysis=None):
    """
    Hesap gizli mi / bot olasılığı tahmini.
    profile_info: fetch_profile_instaloader'dan dönen dict
    engagement_analysis: calculate_engagement_rate çıktısı (opsiyonel)
    """
    is_private = profile_info.get("is_private", False)
    posts = profile_info.get("posts", 0)
    followers = profile_info.get("followers", 0)
    following = profile_info.get("following", 0)
    
    bot_score = 0
    
    # Gizli hesap
    if is_private:
        account_type = "Gizli Hesap"
    else:
        account_type = "Açık Hesap"
    
    # Bot olasılığı basit kurallar
    if posts == 0 and followers > 100:
        bot_score += 2
    if followers > 1000 and engagement_analysis:
        if engagement_analysis.get("engagement_rate", 0) < 1:
            bot_score += 2
    if following > followers * 10:
        bot_score += 1
    
    if bot_score >= 3:
        bot_prediction = "Yüksek olasılıkla bot/pasif hesap"
    elif bot_score == 2:
        bot_prediction = "Orta olasılıkla bot/pasif hesap"
    else:
        bot_prediction = "Doğal aktif hesap"
    
    return {
        "account_type": account_type,
        "bot_prediction": bot_prediction
    }

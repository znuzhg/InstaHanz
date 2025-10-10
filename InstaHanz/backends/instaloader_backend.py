# osi_ig_tool/backends/instaloader_backend.py
import os
import logging
import time
import re
from getpass import getpass

try:
    import instaloader
    from instaloader import Profile, Hashtag, TopSearchResults
except Exception:
    # instaloader yoksa hata fırlatılır; kullanıcıya pip ile yüklemesini söyle
    raise

# Optional: try to use textblob for sentiment if installed; otherwise fallback to simple polarity=0
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except Exception:
    TEXTBLOB_AVAILABLE = False

logger = logging.getLogger(__name__)

# Session klasörü (her giriş için ayrı dosya)
CONFIG_DIR = os.path.expanduser("~/.config/osi_ig_tool/sessions")
os.makedirs(CONFIG_DIR, exist_ok=True)


def _init_loader():
    """Instaloader nesnesi oluştur (minimal ayar)."""
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        save_metadata=False,
        compress_json=False,
    )
    # user-agent değiştirmek istersen burada ayarla: L.context._session.headers.update({...})
    return L


def login_instaloader(username=None):
    """
    Kullanıcı oturumu yönetir.
    - username None ise anonim Instaloader döner
    - username verilirse önce ~/.config/osi_ig_tool/sessions/<username>.session dosyasını yüklemeyi dener
      yoksa parola ister, giriş yapar ve session dosyasını kaydeder
    """
    L = _init_loader()

    if not username:
        logger.info("⚠️ Anonim mod: oturum olmadan çalışılıyor (bazı veri kısıtlı olabilir).")
        return L

    session_file = os.path.join(CONFIG_DIR, f"{username}.session")

    # Eğer kaydedilmiş session varsa yükle
    if os.path.exists(session_file):
        try:
            L.load_session_from_file(username=username, filename=session_file)
            logger.info(f"✅ Session yüklendi: {session_file}")
            return L
        except Exception as e:
            logger.warning(f"⚠️ Session yüklenemedi ({session_file}): {e} — yeni giriş deneniyor.")

    # Yeni giriş işlemi
    password = getpass(f"{username} şifresi: ")
    try:
        L.login(username, password)
        # Kaydetmeyi dene
        try:
            L.save_session_to_file(filename=session_file)
            logger.info(f"🔐 Giriş başarılı, session kaydedildi: {session_file}")
        except Exception as e:
            logger.warning(f"⚠️ Session kaydedilemedi: {e}")
        return L
    except Exception as e:
        logger.error(f"❌ Giriş başarısız: {e}")
        raise


# -----------------------------
# PROFİL BİLGİLERİ
# -----------------------------
def fetch_profile_instaloader(username, login_user=None):
    """
    Gerçek profil bilgilerini döndürür.
    Eğer profil bulunamazsa ValueError fırlatır.
    """
    L = login_instaloader(login_user)
    try:
        profile = Profile.from_username(L.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        raise ValueError(f"Profile bulunamadı: {username}")
    except instaloader.exceptions.ConnectionException as e:
        raise ConnectionError(f"Instagram bağlantı hatası: {e}")
    except Exception as e:
        raise

    data = {
        "username": profile.username,
        "full_name": profile.full_name,
        "biography": profile.biography,
        "external_url": profile.external_url,
        "is_private": profile.is_private,
        "profile_pic_url": profile.profile_pic_url,
        "followers": profile.followers,
        "followees": profile.followees,
        "media_count": profile.mediacount,
    }
    return data


# -----------------------------
# GÖNDERİLER
# -----------------------------
def fetch_posts_instaloader(username, login_user=None, limit=10):
    """
    Kullanıcının gönderilerinin özetini döndürür (url, likes, comments, caption, is_video, date).
    limit: kaç gönderi çekileceği
    """
    L = login_instaloader(login_user)
    profile = Profile.from_username(L.context, username)
    posts = []
    try:
        for i, post in enumerate(profile.get_posts()):
            if i >= limit:
                break
            posts.append({
                "shortcode": post.shortcode,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "likes": getattr(post, "likes", 0),
                "comments": getattr(post, "comments", 0),
                "caption": post.caption if post.caption is not None else None,
                "is_video": getattr(post, "is_video", False),
                "taken_at": post.date_utc.isoformat() if getattr(post, "date_utc", None) else None,
            })
            # Kısa bekleme; büyük ölçekli kullanımda backoff uygulanmalı
            time.sleep(0.2)
    except instaloader.exceptions.ConnectionException as e:
        raise ConnectionError(f"Instagram sorgu hatası: {e}")
    return posts


# -----------------------------
# TAKİPÇİLER
# -----------------------------
def fetch_followers_instaloader(username, login_user=None, limit=20):
    """
    İlk `limit` takipçiyi döndürür (kullanıcı adları).
    """
    L = login_instaloader(login_user)
    profile = Profile.from_username(L.context, username)
    followers = []
    try:
        for i, follower in enumerate(profile.get_followers()):
            if i >= limit:
                break
            followers.append(follower.username)
            time.sleep(0.05)
    except instaloader.exceptions.ConnectionException as e:
        raise ConnectionError(f"Instagram sorgu hatası: {e}")
    return followers


# -----------------------------
# PROFİL FOTOĞRAFI İNDİRME
# -----------------------------
import requests

def download_profile_picture(username, login_user=None, outdir="./downloads"):
    """
    Profil fotoğrafını indirir, dosya yolunu döndürür.
    requests ile indiriliyor, instaloader.download_pic yerine.
    """
    L = login_instaloader(login_user)
    profile = Profile.from_username(L.context, username)
    os.makedirs(outdir, exist_ok=True)
    filename = os.path.join(outdir, f"{username}_profile.jpg")

    try:
        r = requests.get(profile.profile_pic_url, stream=True, timeout=15)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        raise RuntimeError(f"Profil fotoğrafı indirilemedi: {e}")
    return filename



# -----------------------------
# BİYOGRAFİ ANALİZİ (basit)
# -----------------------------
def analyze_bio_text(bio):
    """
    Basit analiz: kelime sayısı, emoji sayısı, link var mı, sentiment (TextBlob varsa).
    """
    if not bio:
        return {"word_count": 0, "emoji_count": 0, "has_link": False, "polarity": 0.0, "sentiment": "neutral"}

    # kelime sayısı
    words = len(bio.split())
    # basit emoji sayısı (unicode range)
    emoji_count = sum(1 for ch in bio if ord(ch) > 10000)  # basit heuristic
    has_link = bool(re.search(r"http[s]?://", bio))

    polarity = 0.0
    sentiment_label = "neutral"
    if TEXTBLOB_AVAILABLE:
        try:
            blob = TextBlob(bio)
            polarity = round(blob.sentiment.polarity, 3)
            sentiment_label = "positive" if polarity > 0.2 else ("negative" if polarity < -0.2 else "neutral")
        except Exception:
            polarity = 0.0
            sentiment_label = "neutral"

    return {
        "word_count": words,
        "emoji_count": emoji_count,
        "has_link": has_link,
        "polarity": polarity,
        "sentiment": sentiment_label
    }


# -----------------------------
# ETKİLEŞİM HESABI
# -----------------------------
def calculate_engagement_rate(posts, followers):
    """
    Basit etkileşim: (avg_likes + avg_comments) / followers * 100
    Dönen dict: avg_likes, avg_comments, engagement_rate
    """
    if not posts or followers == 0:
        return {"avg_likes": 0, "avg_comments": 0, "engagement_rate": 0.0}

    total_likes = sum(p.get("likes", 0) for p in posts)
    total_comments = sum(p.get("comments", 0) for p in posts)
    avg_likes = total_likes / len(posts)
    avg_comments = total_comments / len(posts)
    engagement_rate = ((avg_likes + avg_comments) / followers) * 100
    return {
        "avg_likes": round(avg_likes, 2),
        "avg_comments": round(avg_comments, 2),
        "engagement_rate": round(engagement_rate, 3)
    }


# -----------------------------
# HASHTAG ARAMA
# -----------------------------
def search_hashtag_posts(hashtag, login_user=None, limit=10):
    """
    Hashtag'e göre gönderi arar. Gerçek veri çekmek için instaloader.Hashtag kullanılır.
    """
    L = login_instaloader(login_user)
    posts = []
    try:
        tag = Hashtag.from_name(L.context, hashtag)
        for i, post in enumerate(tag.get_posts()):
            if i >= limit:
                break
            posts.append({
                "shortcode": post.shortcode,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "likes": getattr(post, "likes", 0),
                "caption": post.caption if post.caption is not None else None,
                "taken_at": post.date_utc.isoformat() if getattr(post, "date_utc", None) else None,
            })
            time.sleep(0.2)
    except instaloader.exceptions.QueryReturnedNotFoundException:
        return []
    except Exception as e:
        raise ConnectionError(f"Hashtag sorgu hatası: {e}")
    return posts


# -----------------------------
# KONUM ARAMA
# -----------------------------
def search_location_posts(location_name, login_user=None, limit=10):
    """
    Konum adına göre arama yapar. TopSearchResults kullanılarak ilk uygun lokasyonun gönderileri çekilir.
    """
    L = login_instaloader(login_user)
    posts = []
    try:
        # TopSearchResults sınıfı kullanılarak lokasyon araması
        ts = TopSearchResults(L.context, location_name)
        locations = ts.get_locations()
        if not locations:
            return []
        loc = locations[0]
        for i, post in enumerate(loc.get_posts()):
            if i >= limit:
                break
            posts.append({
                "shortcode": post.shortcode,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "likes": getattr(post, "likes", 0),
                "caption": post.caption if post.caption is not None else None,
                "taken_at": post.date_utc.isoformat() if getattr(post, "date_utc", None) else None,
            })
            time.sleep(0.2)
    except Exception as e:
        raise ConnectionError(f"Konum sorgu hatası: {e}")
    return posts

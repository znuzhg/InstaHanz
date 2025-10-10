import argparse
import logging
from InstaHanz.api import (
    get_user_info,
    get_user_posts_summary,
    get_user_followers,
    get_bio_analysis,
    download_pfp,
    get_engagement_analysis,
    get_hashtag_posts,
    get_location_posts,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    print("""
╔═══════════════════════════════════════╗
║   🧠 InstaHanz v1.0                   ║
║   Instagram OSINT Aracı (by znuzhg)   ║
╚═══════════════════════════════════════╝
[1] Profil Analizi
[2] Hashtag Araması
[3] Konum Araması
[4] Çıkış
""")
    choice = input("Seçiminiz: ")

    if choice == "1":
        user = input("Hedef kullanıcı adı: ")
        backend_user = input("Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): ").strip() or None

        print("\n--- 📄 Profil Bilgileri ---")
        info = get_user_info(username=user, backend_user=backend_user)
        for k, v in info.items():
            print(f"{k}: {v}")

        if input("Biyografi analizi yapmak ister misiniz? (e/h): ").lower() == "e":
            print("\n--- 🧠 Biyografi Analizi ---")
            bio_data = get_bio_analysis(info.get("bio", ""))
            for k, v in bio_data.items():
                print(f"{k}: {v}")

        if input("Profil fotoğrafını indirmek ister misiniz? (e/h): ").lower() == "e":
            print("\n--- 🖼 Profil Fotoğrafı ---")
            filename = download_pfp(user, backend_user=backend_user)
            print(f"Kaydedildi: {filename}")

        if input("Takipçileri listelemek ister misiniz? (e/h): ").lower() == "e":
            print("\n--- 👥 Takipçiler (ilk 20) ---")
            followers = get_user_followers(user, backend_user=backend_user)
            for f in followers:
                print(f"- {f}")

        if input("Gönderileri listelemek ister misiniz? (e/h): ").lower() == "e":
            print("\n--- 📸 Gönderiler ---")
            posts = get_user_posts_summary(username=user, backend_user=backend_user)
            for i, post in enumerate(posts, 1):
                print(f"\n[{i}] ❤️ {post.get('likes', 0)} | 💬 {post.get('comments', 0)}")
                print(f"URL: {post.get('url', 'Bilinmiyor')}")
                caption = post.get("caption")
                if caption:
                    print(f"Caption: {caption[:100]}...")

        if input("Etkileşim oranı analizi yapmak ister misiniz? (e/h): ").lower() == "e":
            print("\n--- 📊 Etkileşim Analizi ---")
            posts = get_user_posts_summary(username=user, backend_user=backend_user, limit=10)
            analysis = get_engagement_analysis(posts, info.get("followers", 0))
            for k, v in analysis.items():
                print(f"{k}: {v}")

    elif choice == "2":
        hashtag = input("Hashtag giriniz (örn: istanbul): ").strip()
        backend_user = input("Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): ").strip() or None
        limit = int(input("Gösterilecek gönderi sayısı (default 10): ") or 10)
        print(f"\n--- 🔍 Hashtag Araması: #{hashtag} ---")
        posts = get_hashtag_posts(hashtag, backend_user=backend_user, limit=limit)
        for i, post in enumerate(posts, 1):
            print(f"\n[{i}] ❤️ {post.get('likes', 0)}")
            print(f"URL: {post.get('url', 'Bilinmiyor')}")
            caption = post.get("caption")
            if caption:
                print(f"Caption: {caption[:100]}...")

    elif choice == "3":
        location = input("Konum giriniz (örn: Ankara): ").strip()
        backend_user = input("Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): ").strip() or None
        limit = int(input("Gösterilecek gönderi sayısı (default 10): ") or 10)
        print(f"\n--- 🌍 Konum Araması: {location} ---")
        posts = get_location_posts(location, backend_user=backend_user, limit=limit)
        for i, post in enumerate(posts, 1):
            print(f"\n[{i}] ❤️ {post.get('likes', 0)}")
            print(f"URL: {post.get('url', 'Bilinmiyor')}")
            caption = post.get("caption")
            if caption:
                print(f"Caption: {caption[:100]}...")

    elif choice == "4":
        print("Çıkış yapılıyor...")
        return
    else:
        print("⚠️ Geçersiz seçim!")

if __name__ == "__main__":
    main()

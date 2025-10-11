#!/usr/bin/env python3
from InstaHanz.api import (
    get_user_info,
    get_user_posts_summary,
    get_user_followers,
    download_pfp,
    get_bio_analysis,
    get_engagement_analysis,
    get_hashtag_posts,
    get_location_posts,
    get_account_prediction
)

def main():
    print("╔═══════════════════════════════════════╗")
    print("║   🧠 InstaHanz v1.0                   ║")
    print("║   Instagram OSINT Aracı (by znuzhg)   ║")
    print("╚═══════════════════════════════════════╝")
    print()
    print("[1] Profil Analizi")
    print("[2] Hashtag Araması")
    print("[3] Konum Araması")
    print("[4] Çıkış\n")
    choice = input("Seçiminiz: ").strip()

    backend_user = None
    if choice == "1":
        username = input("Hedef kullanıcı adı: ").strip()
        backend_user = input("Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): ").strip() or None

        info = get_user_info(username, backend_user)
        print("\n--- 📄 Profil Bilgileri ---")
        for k,v in info.items():
            print(f"{k}: {v}")

        if input("Biyografi analizi yapmak ister misiniz? (e/h): ").lower() == "e":
            bio_res = get_bio_analysis(info.get("biography",""))
            print("\n--- 🧠 Biyografi Analizi ---")
            for k,v in bio_res.items():
                print(f"{k}: {v}")

        if input("Profil fotoğrafını indirmek ister misiniz? (e/h): ").lower() == "e":
            try:
                filename = download_pfp(username, backend_user)
                print(f"\nKaydedildi: {filename}")
            except Exception as e:
                print(f"\n❌ Profil fotoğrafı indirilemedi: {e}")

        if input("Takipçileri listelemek ister misiniz? (e/h): ").lower() == "e":
            try:
                followers = get_user_followers(username, backend_user, limit=20)
                print("\n--- 👥 Takipçiler (ilk 20) ---")
                for f in followers:
                    print(f"- {f}")
            except Exception as e:
                print(f"\n❌ Takipçi bilgileri alınamadı: {e}")

        if input("Gönderileri listelemek ister misiniz? (e/h): ").lower() == "e":
            posts = get_user_posts_summary(username, backend_user, limit=5)
            print("\n--- 📸 Gönderiler ---\n")
            for i, post in enumerate(posts, 1):
                caption = post.get("caption","")
                print(f"[{i}] ❤️ {post.get('likes',0)} | 💬 {post.get('comments',0)}")
                print(f"URL: {post.get('url','')}")
            if input("Etkileşim analizi yapmak ister misiniz? (e/h): ").lower() == "e":
                engagement = get_engagement_analysis(posts, info.get("followers",1))
                print("\n--- 📊 Etkileşim Analizi ---")
                print(engagement)
            if input("AI tabanlı hesap tahmini yapmak ister misiniz? (e/h): ").lower() == "e":
                pred = get_account_prediction(info, engagement_analysis=engagement)
                print("\n--- 🤖 Hesap Tahmini ---")
                print(pred)

    elif choice == "2":
        hashtag = input("Hashtag giriniz (örn: istanbul): ").strip()
        backend_user = input("Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): ").strip() or None
        limit = int(input("Gösterilecek gönderi sayısı (default 10): ") or 10)
        try:
            posts = get_hashtag_posts(hashtag, backend_user, limit)
            print(f"\n--- 🔍 Hashtag Araması: #{hashtag} ---")
            for i, post in enumerate(posts,1):
                print(f"[{i}] ❤️ {post.get('likes',0)} | 💬 {post.get('comments',0)}")
                print(f"URL: {post.get('url','')}")
        except Exception as e:
            print(f"\n❌ Hashtag sorgu hatası: {e}")

    elif choice == "3":
        location = input("Konum (örn: Ankara): ").strip()
        backend_user = input("Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): ").strip() or None
        limit = int(input("Kaç gönderi gösterilsin? (örn: 10): ") or 10)
        try:
            posts = get_location_posts(location, backend_user, limit)
            print(f"\n--- 🔍 Konum Araması: {location} ---")
            for i, post in enumerate(posts,1):
                print(f"[{i}] ❤️ {post.get('likes',0)} | 💬 {post.get('comments',0)}")
                print(f"URL: {post.get('url','')}")
        except Exception as e:
            print(f"\n❌ Konum sorgu hatası: {e}")

    elif choice == "4":
        exit()
    else:
        print("Geçersiz seçenek!")

if __name__ == "__main__":
    main()

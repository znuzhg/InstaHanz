#!/bin/bash
clear

BANNER="
╔═══════════════════════════════════════╗
║   🧠 InstaHanz v1.0                   ║
║   Instagram OSINT Aracı (by Mahmut)   ║
╚═══════════════════════════════════════╝
"
echo "$BANNER"

while true; do
    echo ""
    echo "[1] Profil Analizi"
    echo "[2] Hashtag Araması"
    echo "[3] Konum Araması"
    echo "[4] Çıkış"
    echo ""
    read -p "Seçiminiz: " choice

    case $choice in
        1)
            read -p "Hedef kullanıcı adı: " user
            read -p "Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): " login
            echo "--- Profil Analizi Başlatılıyor ---"
            python3 -m InstaHanz profile -u "$user" --posts --followers --bio-analyze --engagement --download-pfp --login "$login"
            ;;
        2)
            read -p "Hashtag (örn: istanbul): " tag
            read -p "Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): " login
            read -p "Kaç gönderi gösterilsin? (örn: 10): " limit
            echo "--- Hashtag Araması Başlatılıyor ---"
            python3 -m InstaHanz search --hashtag "$tag" --limit "$limit" --login "$login"
            ;;
        3)
            read -p "Konum (örn: Ankara): " loc
            read -p "Kendi hesabınızla giriş yapacak mısınız? (boş bırakabilirsiniz): " login
            read -p "Kaç gönderi gösterilsin? (örn: 10): " limit
            echo "--- Konum Araması Başlatılıyor ---"
            python3 -m InstaHanz search --location "$loc" --limit "$limit" --login "$login"
            ;;
        4)
            echo "Çıkış yapılıyor..."
            exit 0
            ;;
        *)
            echo "⚠️  Geçersiz seçim, tekrar deneyin."
            ;;
    esac

    echo ""
    read -p "Devam etmek için [Enter] tuşuna basın..." dummy
    clear
    echo "$BANNER"
done

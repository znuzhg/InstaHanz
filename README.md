<<<<<<< HEAD
# InstaHanz
InstaHanz Instagram OSINT Aracı - Profil, Hashtag ve Konum Analizi için CLI Aracı
=======
# 🧠 InstaHanz v1.0

Instagram OSINT Aracı (by znuzhg)

---

## ⚡ Araç Hakkında

**InstaHanz v1.0**, Instagram üzerinde OSINT (Open Source Intelligence) teknikleri kullanarak profil analizi, takipçi ve gönderi takibi, hashtag ve konum aramaları yapmanıza olanak tanır. Araç tamamen Python ile geliştirilmiştir ve kolay kullanımlı bir CLI arayüzüne sahiptir.

---

## 📦 Özellikler

- Profil Analizi
  - Kullanıcı adı, tam ad, biyografi, takipçi/ takip edilen sayısı, gönderi sayısı
  - Biyografi analizi (kelime sayısı, emoji sayısı, bağlantı durumu, duygu analizi)
  - Profil fotoğrafı indirme
- Takipçi ve Takip Edilen Listeleme
- Gönderi Analizi
  - Beğeni ve yorum sayıları
  - Etkileşim oranı hesaplama
- Hashtag Arama
  - Belirli hashtag ile paylaşılan gönderileri listeleme
- Konum Arama
  - Belirli konumda paylaşılan gönderileri listeleme
- AI Destekli Hesap Tahmini
  - Hesabın bot mu yoksa doğal aktif bir hesap mı olduğunu tahmin eder

---

## ⚙️ Kurulum

1. Depoyu klonlayın:

```bash
git clone https://github.com/znuzhg/InstaHanz.git
cd InstaHanz
chmod +x InstaHanz.sh InstaHanz_launcher.py
#Sanal ortam oluşturun ve aktif edin:

python3 -m venv instavenv
source instavenv/bin/activate

#Gerekli paketleri yükleyin:
python3 -m pip install -r requirements.txt

#setup.py için gerekli
pip install --upgrade pip setuptools wheel

#Aracı başlatmak için:
python3 InstaHanz_launcher.py
veya
./InstaHanz.sh
############################################################################################
# Not: Hashtag ve konum aramaları için Instagram hesabınızla giriş yapmanız gerekmektedir. #
#      Giriş yapılmadan bu veriler alınamaz.                                               #
############################################################################################

💡 Dikkat Edilecek Noktalar

Takipçi listesi, hashtag ve konum verileri giriş yapılmadan alınamaz.

Profil gizlilik ayarları (private account) bazı bilgilerin alınmasını kısıtlayabilir.

Araç eğitim ve araştırma amaçlıdır, etik kurallar çerçevesinde kullanılmalıdır.

#📁 Dosya Yapısı
InstaHanz/
├── main.py
├── api.py
├── backends/
│ ├── instaloader_backend.py
│ └── ai_analysis.py
├── pycache/
InstaHanz_launcher.py
InstaHanz.sh
requirements.txt
README.md
setup.py
downloads/
instavenv/

#📜 Lisans
InstaHanz, MIT Lisansı ile lisanslanmıştır.
Kendi araştırmalarınızda ve eğitim amaçlı kullanabilirsiniz.
#💻 Öneriler
Python 3.10+ önerilir.
Sanal ortam kullanımı tavsiye edilir.
Instagram API’si zaman zaman değişebilir; hatalar için güncelleme gerekebilir.
>>>>>>> 10e2107 (InstaHanz v1.0 - İlk sürüm)

# ⭐ Yer İmi Oluşturucu & Dönüştürücü (Bookmark HTML Converter)
## _Canlı Ortam - Production Environment_


✨ Kişisel yer imlerinizi (bookmarks) modern, şık ve mobil uyumlu bir HTML sayfasına dönüştürün veya sıfırdan kendi bookmark dosyanızı oluşturun! 
**Tamamen ücretsiz, reklamsız ve limitsiz.** Türkçe ve İngilizce dil desteğiyle, tüm cihaz ve tarayıcılarda sorunsuz çalışır.

[![Canlı Demo (Frontend)](https://img.shields.io/badge/Netlify-Live-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://bookmark-converter.netlify.app)
[![Backend (Render)](https://img.shields.io/badge/Render-Backend-1976d2?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/osmandemir2533/Bookmark-Converter)

---

## 📁 Proje Dizini

```
bookmarks/
├── app.py                      # Flask backend (API)
├── convert_bookmarks_web.py    # Bookmark dönüştürme motoru
├── requirements.txt            # Python bağımlılıkları
├── templates/
│   └── index.html              # Ana frontend arayüzü
├── uploads/                    # Geçici yüklenen dosyalar
├── outputs/                    # Geçici çıktı dosyaları
├── .gitignore                  # uploads/ ve outputs/ içeriği hariç tutar
└── README.md                   # Proje dokümantasyonu
```

---

## 🚀 Canlı Kullanım

- **Frontend (Kullanıcı Arayüzü):**  [Bookmark Converter](https://bookmark-converter.netlify.app)
- **Backend (API)** 

---

## ✨ Özellikler

- 🆕 **Sıfırdan Bookmark HTML Dosyası Oluşturma:**
  - Klasör ve bağlantı ekleyerek kendi bookmark dosyanızı oluşturun.
  - Oluşturulan dosya, Chrome, Firefox, Edge, Opera ve tüm modern tarayıcılara uyumludur.
  - Dilediğiniz zaman tarayıcınıza yükleyip, istediğiniz cihazda kullanabilirsiniz.

- 🎨 **Stil Dönüştürücü (Bookmark Beautifier):**
  - Mevcut bir bookmark HTML dosyasını yükleyin, modern ve kullanıcı dostu bir görünüme kavuşturun.
  - Tüm çıktı dosyaları mobil uyumlu ve responsive'dır.
  - Dönüştürülen dosyayı telefonunuzda, bilgisayarınızda veya tabletinizde açabilirsiniz.

- 🌐 **Çoklu Dil Desteği:**
  - Türkçe ve İngilizce arayüz.
  - Tüm hata ve bilgi mesajları iki dilde.

- 📱 **Mobil ve Masaüstü Uyumluluğu:**
  - Tüm cihazlarda (iOS, Android, Windows, Mac, Linux) sorunsuz çalışır.
  - Responsive ve modern tasarım.

- 👤 **Kullanıcı Odaklı:**
  - Hiçbir kişisel veri kaydedilmez.
  - Dosyalarınız sadece kısa süreli olarak sunucuda tutulur ve otomatik silinir.

- ⚡ **Kolay Entegrasyon:**
  - Dilerseniz kendi Netlify/Render hesabınızda yayına alabilirsiniz.

---

## 🛠️ Kullanılan Teknolojiler

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python (Flask), BeautifulSoup4
- **Hosting:** Netlify (frontend), Render (backend)
- **Ekstra:** flask-cors, gunicorn

---

## ⚡ Hızlı Başlangıç (Lokal Geliştirme)

### Gereksinimler
- Python 3.7+
- pip

### Kurulum ve Çalıştırma

```bash
# Repoyu klonlayın
git clone https://github.com/senin-repo-linkin.git
cd bookmarks

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Geliştirme sunucusunu başlatın
python app.py

# veya production için:
gunicorn app:app

#Tarayıcıda açın:
`http://localhost:5000`
```

---


## 🖼️ Arayüz (UI)

Uygulama arayüzü iki ana bölümden oluşur: Sol tarafta sıfırdan yer imi oluşturucu, sağ tarafta ise mevcut HTML dosyasını stilize eden dönüştürücü bulunur. Tüm sayfa modern, responsive ve mobil uyumlu olarak tasarlanmıştır. Kullanıcılar diledikleri dilde, cihazda ve tarayıcıda kolayca işlem yapabilirler.

<p align="center">
  <img src="https://i.imgur.com/1kT3A0q.png" width="900"/>
</p>
<p align="center">
  <img src="https://i.imgur.com/6nXIzFn.png" width="900"/>
</p>

---

### 1️⃣ Sıfırdan Yer İmi Oluşturucu (Sol Kutu)

- Klasör ve bağlantı ekleyerek kendi bookmark dosyanızı oluşturun.
- Sürükle-bırak, otomatik başlık çekme, isimsiz bağlantı ekleme gibi gelişmiş özellikler.
- Oluşturulan dosyayı tek tıkla indirin.

<p align="center">
  <img src="https://i.imgur.com/EdKP2Am.png" width="400"/>
</p>

- Örnek HTML Çıktı:

<p align="center">
  <img src="https://i.imgur.com/IWFkxiN.png" width="200"/>
</p>

---

### 2️⃣ Stil Dönüştürücü (Sağ Kutu)

- Mevcut bir bookmark HTML dosyasını yükleyin.
- Adınızı girin, "Dönüştür" butonuna tıklayın.
- Modern, mobil uyumlu ve kullanıcı dostu bir HTML dosyası anında oluşturulur.
- Dönüştürülen dosyayı tek tıkla indirin.

<p align="center">
  <img src="https://i.imgur.com/ZMgHhjS.png" width="500"/>
</p>

- Örnek HTML Çıktı:

<p align="center">
  <img src="https://i.imgur.com/SddpkjA.png" width="600"/>
</p>

---

### 📱 Mobil ve Tüm Cihazlarda Görünüm

- Arayüz tamamen responsive ve mobil uyumludur.
- Tüm cihazlarda (telefon, tablet, bilgisayar) sorunsuz çalışır.

<p align="center">
  <img src="https://i.imgur.com/udMdVDB.png" width="300"/>
   
  <img src="https://i.imgur.com/G7EMzq7.png" width="300"/>
</p>


---

## 🖥️ Kullanım Senaryoları

### 1. Sıfırdan Bookmark HTML Dosyası Oluşturma
- Sol kutudan klasör ve bağlantılar ekleyin.
- "Oluştur" ve ardından "İndir" butonuna tıklayın.
- Oluşan dosyayı Chrome, Firefox, Edge, Opera ve diğer tüm tarayıcılara yükleyebilirsiniz.
- Dosya tamamen standart bookmark formatında, **her tarayıcıda uyumlu**.

### 2. Mevcut Bookmark HTML Dosyasını Stilize Etme
- Sağ kutudan mevcut bir bookmark HTML dosyasını yükleyin.
- Adınızı girin, "Dönüştür" butonuna tıklayın.
- Modern, mobil uyumlu ve kullanıcı dostu bir HTML dosyası anında oluşturulur.
- Dönüştürülen dosyayı telefonunuzda, bilgisayarınızda veya tabletinizde açabilirsiniz.

### 3. Mobil ve Tüm Cihazlarda Kullanım
- Oluşturulan veya dönüştürülen HTML dosyası, **tüm cihazlarda** (iOS, Android, Windows, Mac, Linux) ve tarayıcılarda açılabilir.
- Dilerseniz dosyayı telefonunuza kaydedip, ana ekrana kısayol olarak ekleyebilirsiniz.

---

## 🔒 Güvenlik ve Gizlilik

- Yüklediğiniz dosyalar **sadece geçici olarak** sunucuda tutulur, 5 dakika veya 24 saat sonra otomatik silinir.
- Hiçbir kişisel veri kaydedilmez, paylaşılmaz.
- Tamamen açık kaynak ve şeffaf.

---

## 🌍 Dil Desteği

- **Türkçe ve İngilizce** arayüz.
- Tüm hata ve bilgi mesajları iki dilde.
- Dilerseniz arayüzden anında dil değiştirebilirsiniz.
- Seçilen dile göre, oluşturulan veya dönüştürülen HTML dosyasının **dosya adı** ve içeriğindeki başlık/metinler otomatik olarak o dile uygun şekilde düzenlenir. Böylece hem dosya isimleri hem de kullanıcıya sunulan arayüz ve çıktı, seçilen dile tamamen uyumlu olur.

---

## 📝 Sıkça Sorulan Sorular

**S: Oluşturduğum/dönüştürdüğüm dosyayı Chrome/Firefox/Edge'de kullanabilir miyim?**  
C: Evet! Dosya tamamen standart bookmark formatında, tüm modern tarayıcılarla uyumludur.

**S: Dosyamı yükledikten sonra başkası görebilir mi?**  
C: Hayır, dosyanız sadece kısa süreli olarak sunucuda tutulur ve otomatik silinir.

**S: Mobilde kullanabilir miyim?**  
C: Evet, arayüz ve çıktı dosyaları tamamen mobil uyumludur.

---

## 🛠️ Teknik Detaylar

- **Backend:**  
  - Flask ile REST API
  - CORS desteği (flask-cors)
  - Production için gunicorn ile çalıştırılır
  - outputs/ ve uploads/ klasörleri otomatik temizlenir (5 dakika ve 24 saatlik periyotlarla)
- **Frontend:**  
  - Tamamen statik, Netlify veya başka bir statik hostingde çalışır
  - API çağrıları backend'e yönlendirilir
  - Responsive ve modern tasarım
  - Türkçe/İngilizce dil desteği

---

## 📬 İletişim

**Osman Demir**  
[![Web Sitem](https://img.shields.io/badge/Web%20Site-1976d2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://osmandemir2533.github.io/)  [![LinkedIn](https://img.shields.io/badge/LinkedIn-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/osmandemir2533/)  [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/osmandemir2533)

---

> Proje, modern web standartlarına uygun olarak geliştirilmiştir.  
> Responsive tasarımı ile tüm cihazlarda sorunsuz çalışır.  
> Tamamen açık kaynak ve ücretsizdir. 
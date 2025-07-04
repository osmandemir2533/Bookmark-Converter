# 🔖 Yer İşaretleri Dönüştürücü

Chrome yer işaretlerinizi güzel ve modern bir görünüme kavuşturan web uygulaması.

## ✨ Özellikler

- 🎨 Modern ve responsive tasarım
- 📁 Drag & drop dosya yükleme
- 🔄 Otomatik favicon yükleme
- 📱 Mobil uyumlu
- ⚡ Hızlı dönüştürme
- 🎯 Kullanıcı dostu arayüz

## 🚀 Kurulum

### Gereksinimler
- Python 3.7+
- pip

### Adımlar

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd yer-isaretleri-donusturucu
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı çalıştırın:**
```bash
python app.py
```

4. **Tarayıcınızda açın:**
```
http://localhost:5000
```

## 📖 Kullanım

1. **Chrome'da yer işaretlerinizi dışa aktarın:**
   - `Ctrl+Shift+O` tuşlarına basın
   - Sağ üst köşedeki ⋮ menüsüne tıklayın
   - "Yer işaretlerini dışa aktar" seçeneğini seçin
   - HTML dosyasını bilgisayarınıza kaydedin

2. **Web uygulamasında:**
   - İsim ve soyisminizi girin
   - İndirdiğiniz HTML dosyasını yükleyin
   - "Dönüştür" butonuna tıklayın
   - Güzel görünümlü dosyanızı indirin!

## 🛠️ Teknolojiler

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **HTML Parsing:** BeautifulSoup4
- **Stil:** Modern CSS Grid & Flexbox
- **Font:** Inter (Google Fonts)

## 📁 Proje Yapısı

```
yer-isaretleri-donusturucu/
├── app.py                 # Flask uygulaması
├── convert_bookmarks.py   # Dönüştürme motoru
├── requirements.txt       # Python bağımlılıkları
├── templates/
│   └── index.html        # Ana sayfa template'i
├── uploads/              # Geçici dosya yükleme klasörü
└── outputs/              # Geçici çıktı klasörü
```

## 🔧 Geliştirme

### Yerel Geliştirme
```bash
# Geliştirme modunda çalıştır
python app.py

# Debug modunda çalıştır
export FLASK_ENV=development
flask run
```

### Production Deployment
```bash
# Gunicorn ile production'da çalıştır
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**Osman Demir**
- Website: [osmandemir2533.github.io](https://osmandemir2533.github.io)
- GitHub: [@osmandemir2533](https://github.com/osmandemir2533)

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 🐛 Hata Bildirimi

Bir hata bulduysanız, lütfen [GitHub Issues](https://github.com/osmandemir2533/yer-isaretleri-donusturucu/issues) sayfasında bildirin.

## 📈 Gelecek Özellikler

- [ ] Diğer tarayıcı desteği (Firefox, Safari)
- [ ] Tema seçenekleri
- [ ] Yer işareti kategorileri
- [ ] Arama özelliği
- [ ] Sosyal medya paylaşımı

## 💡 İlham

Bu proje, Chrome yer işaretlerinin düz HTML formatından daha güzel ve kullanışlı bir görünüme kavuşturulması ihtiyacından doğmuştur.

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 
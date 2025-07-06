from flask import Flask, render_template, request, send_file, jsonify, abort
import os
import tempfile
from werkzeug.utils import secure_filename
import uuid
import threading
import time
import unicodedata
import logging
from flask_cors import CORS
import shutil

# Sadece convert_bookmarks_web modülünü import et
from convert_bookmarks_web import convert_bookmarks_to_html

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Klasörleri oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    counter_path = file_path + '.downloads'
    if not os.path.exists(file_path):
        return jsonify({'error': 'file_not_found'}), 404
    # Sayaç dosyasını oku/artır
    count = 0
    if os.path.exists(counter_path):
        with open(counter_path, 'r') as f:
            try:
                count = int(f.read())
            except:
                count = 0
    count += 1
    with open(counter_path, 'w') as f:
        f.write(str(count))
    # 10. indirmeden sonra dosya ve sayaç silinsin
    if count >= 10:
        try:
            os.remove(file_path)
        except Exception: pass
        try:
            os.remove(counter_path)
        except Exception: pass
    return send_file(file_path, as_attachment=True)

# --- outputs klasörünü beş dakikada temizleyen fonksiyon ---
def clean_outputs_folder():
    while True:
        now = time.time()
        folder = app.config['OUTPUT_FOLDER']
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            try:
                if os.path.isfile(fpath):
                    age = now - os.path.getmtime(fpath)
                    if age > 300:  # 5 dakika
                        print(f"{fname} silme işlemi başlatıldı.")
                        os.remove(fpath)
                        print(f"{fname} silindi.")
            except Exception as e:
                pass
        time.sleep(300)  # 5 dakikada bir çalışsın

# Temizlik threadini başlat
threading.Thread(target=clean_outputs_folder, daemon=True).start()

# --- outputs klasörünü her gün temizleyen fonksiyon ---
def clean_outputs_folder_daily():
    while True:
        folder = app.config['OUTPUT_FOLDER']
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            try:
                if os.path.isfile(fpath):
                    os.remove(fpath)
            except Exception:
                pass
        time.sleep(86400)  # 24 saat (60*60*24)

# Günlük temizlik threadini başlat
threading.Thread(target=clean_outputs_folder_daily, daemon=True).start()

# --- uploads klasörünü her gün temizleyen fonksiyon ---
def clean_uploads_folder_daily():
    while True:
        folder = app.config['UPLOAD_FOLDER']
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            try:
                if os.path.isfile(fpath):
                    os.remove(fpath)
                elif os.path.isdir(fpath):
                    shutil.rmtree(fpath)
            except Exception:
                pass
        time.sleep(86400)  # 24 saat (60*60*24)

# Günlük uploads temizlik threadini başlat
threading.Thread(target=clean_uploads_folder_daily, daemon=True).start()

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.lower().replace(' ', '_')
    value = ''.join(c for c in value if c.isalnum() or c == '_')
    return value

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Form verilerini al
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        lang = request.form.get('lang', 'tr').strip()
        
        # Dosya kontrolü
        if 'bookmarks_file' not in request.files:
            return jsonify({'error': 'no_file_selected'}), 400
        
        file = request.files['bookmarks_file']
        if file.filename == '':
            return jsonify({'error': 'no_file_selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'only_html_allowed'}), 400
        
        # Benzersiz dosya adı oluştur
        unique_id = str(uuid.uuid4())
        input_filename = f"bookmarks_{unique_id}.html"
        # Dosya adı: yer_isaretleri_isim_soyisim.html veya bookmarks_isim_soyisim.html
        base = 'bookmarks' if lang == 'en' else 'yer_isaretleri'
        name_part = slugify(f"{first_name}_{last_name}") if (first_name or last_name) else 'kullanici'
        output_filename = f"{base}_{name_part}.html"
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Dosyayı kaydet
        file.save(input_path)
        
        # Dönüştürme işlemi
        full_name = f"{first_name} {last_name}".strip()
        if not full_name:
            full_name = "Kullanıcı"
        
        success = convert_bookmarks_to_html(input_path, output_path, full_name, lang)
        
        if success:
            # Sayaç dosyasını başlat (ilk indirme için)
            with open(output_path + '.downloads', 'w') as f:
                f.write('0')
            # Kullanıcıya çıktı dosyasının adını dön
            return jsonify({'filename': output_filename})
        else:
            return jsonify({'error': 'convert_failed'}), 500
            
    except Exception as e:
        return jsonify({'error': 'convert_failed'}), 500
    
    finally:
        # Geçici dosyaları temizle
        try:
            if 'input_path' in locals() and os.path.exists(input_path):
                os.remove(input_path)
        except:
            pass

# Local Geliştirme Ortamı için aşağıdaki kodları(185-186) yorum satırlarını kaldır terminalde python app.py yaz
# Canlıya almak istersen aşağıdaki kodları(185-186) yorum satırına al gunicorn app:app ile Render da çalışır sadece
#if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5000)
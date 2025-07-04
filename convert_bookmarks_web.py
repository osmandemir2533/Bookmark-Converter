import os
from html import escape
from bs4 import BeautifulSoup
import re
import unicodedata

def normalize_tr(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

def get_favicon(url):
    try:
        if '://' in url:
            domain = url.split('/')[2]
        else:
            domain = url.split('/')[0]
        
        if domain.startswith('www.'):
            domain = domain[4:]
        
        favicon_url = f'https://www.google.com/s2/favicons?domain={domain}'
        return favicon_url
    except:
        return 'https://img.icons8.com/fluency/48/link.png'  # default link icon

FOLDER_ICON = 'https://img.icons8.com/fluency/48/folder-invoices.png'

def is_icon_only(a):
    title = a.get_text().strip()
    return (not title) or len(title) <= 0

def get_all_dt_elements(dl):
    dt_elements = []
    dl_html = dl.decode_contents()
    dt_blocks = re.split(r'(?i)(?=<DT>)', dl_html)
    for block in dt_blocks:
        if block.strip().lower().startswith('<dt>'):
            soup = BeautifulSoup(block, 'html.parser')
            dt = soup.find('dt')
            if dt:
                dt_elements.append(dt)
    return dt_elements

def parse_dl(dl, icon_only_links, root_links=None, folder_links=None, is_root=True, icon_only_urls=None):
    if icon_only_urls is None:
        icon_only_urls = set()
    left_html = ''
    right_html = ''
    seen_folders = set()
    for dt in dl.find_all('dt', recursive=True):
        h3 = dt.find('h3')
        if h3:
            folder_name = escape(h3.get_text().strip())
            if normalize_tr(folder_name) in ["yer isaretleri cubugu"]:
                continue
            if folder_name in seen_folders:
                continue
            seen_folders.add(folder_name)
            sub_dl = dt.find('dl')
            children_html = ''
            if sub_dl:
                left, right = parse_dl(sub_dl, icon_only_links, root_links, folder_links, is_root=False, icon_only_urls=icon_only_urls)
                children_html = left + right
            if children_html.strip():
                folder_html = f'<details><summary><img class="folder-icon" src="{FOLDER_ICON}" alt="klasör"/> {folder_name}</summary><ul class="bookmark-list">{children_html}</ul></details>'
                left_html += folder_html
        else:
            a = dt.find('a')
            if a:
                url = a.get('href', '#')
                title = escape(a.get_text().strip())
                icon = a.get('ICON') or a.get('icon')
                favicon = icon if icon and icon.startswith('data:') else get_favicon(url)
                if is_icon_only(a):
                    if url not in icon_only_urls:
                        icon_only_links.append((favicon, url, title))
                        icon_only_urls.add(url)
                    if is_root:
                        continue  # kökteyse sadece icon bar'a ekle, kökte gösterme
                    # klasördeyse hem icon bar'a hem klasör içinde göster
                if is_root:
                    # Kökteyiz, eğer bu url klasörlerde varsa ekleme
                    if folder_links is not None and url in folder_links:
                        continue
                    if root_links is not None:
                        root_links.add(url)
                    right_html += f'<li class="bookmark-card"><a href="{escape(url)}" target="_blank" rel="noopener"><img class="favicon" src="{favicon}" alt="favicon"/><span class="bookmark-title">{title}</span></a></li>'
                else:
                    # Klasördeyiz, eğer bu url kökte varsa ekleme
                    if root_links is not None and url in root_links:
                        continue
                    if folder_links is not None:
                        folder_links.add(url)
                    right_html += f'<li class="bookmark-card"><a href="{escape(url)}" target="_blank" rel="noopener"><img class="favicon" src="{favicon}" alt="favicon"/><span class="bookmark-title">{title}</span></a></li>'
    return left_html, right_html

def sort_bookmarks_soup(soup):
    """
    Verilen BeautifulSoup objesinin kök <DL>'sini önce klasörler, sonra kök yer imleri olacak şekilde hafızada sıralar.
    Aynı soup objesini döndürür.
    """
    dl = soup.find('dl')
    if not dl:
        return soup
    dt_list = [dt for dt in dl.find_all('dt', recursive=True)]
    folders = []
    root_items = []
    for dt in dt_list:
        if dt.find('h3'):
            folders.append(dt)
        elif dt.find('a'):
            root_items.append(dt)
    new_dl = soup.new_tag('dl')
    for dt in folders + root_items:
        new_dl.append(dt)
        next_sib = dt.find_next_sibling()
        while next_sib and (next_sib.name == 'dl' or (next_sib.name == 'p' and not next_sib.text.strip())):
            new_dl.append(next_sib)
            next_sib = next_sib.find_next_sibling()
    dl.replace_with(new_dl)
    return soup

def sort_bookmarks_manual(soup):
    """
    Kök DL'deki DT'leri:
    1. Klasörler (DT > H3)
    2. Kökteki isimsiz/ikonik yer imleri (DT > A, başlığı yok)
    3. Kökteki isimli yer imleri (DT > A, başlığı var)
    sırasına göre dizer.
    """
    dl = soup.find('dl')
    if not dl:
        return soup
    all_dt = dl.find_all('dt', recursive=True)
    root_dt = [dt for dt in all_dt if dt.find_parent('dl') is dl]
    folders = []
    iconics = []
    named = []
    for dt in root_dt:
        h3 = dt.find('h3')
        a = dt.find('a')
        if h3:
            folders.append(dt)
        elif a:
            title = a.get_text().strip()
            if not title:
                iconics.append(dt)
            else:
                named.append(dt)
    new_dl = soup.new_tag('dl')
    for dt in folders + iconics + named:
        new_dl.append(dt)
        # Klasörse, hemen arkasındaki DL ve P'yi de ekle
        if dt.find('h3'):
            sib = dt.find_next_sibling()
            while sib and (sib.name == 'dl' or (sib.name == 'p' and not sib.text.strip())):
                new_dl.append(sib)
                sib = sib.find_next_sibling()
    dl.replace_with(new_dl)
    return soup

def convert_bookmarks_to_html(input_file, output_file, user_name="Kullanıcı", lang="tr"):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        soup = sort_bookmarks_manual(soup)
        dl = soup.find('dl')
        if not dl:
            title_text = "Bookmarks" if lang == "en" else "Yer İmlerim"
            html = f'''<!DOCTYPE html>\n<html lang="{lang}">\n<head><meta charset="UTF-8"><title>{title_text}</title></head><body><p>Hiç yer imi bulunamadı.</p></body></html>'''
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            return True

        icon_only_links = []
        root_links = set()
        folder_links = set()
        left_html, right_html = parse_dl(dl, icon_only_links, root_links, folder_links, is_root=True, icon_only_urls=set())
        # Klasör ve kök yer imi olup olmadığını tespit et
        has_folders = bool(left_html.strip())
        has_root = bool(right_html.strip())
        if has_folders and has_root:
            grid_class = "both"
        elif has_folders:
            grid_class = "only-folders"
        elif has_root:
            grid_class = "only-root"
        else:
            grid_class = "none"
        icon_bar_html = ''
        for favicon, url, title in icon_only_links:
            if not favicon:
                favicon = 'https://img.icons8.com/fluency/48/link.png'
            icon_bar_html += f'<a class="icon-bar-item" href="{escape(url)}" target="_blank" rel="noopener"><img class="icon-bar-favicon" src="{favicon}" alt="favicon"/></a>'

        if icon_bar_html:
            icon_bar_section = \
                '<div class="icon-bar-wrapper">\n' \
                '<div class="icon-bar-arrow left">&#x2039;</div>\n' \
                '<div class="icon-bar">' + icon_bar_html + '</div>\n' \
                '<div class="icon-bar-arrow right">&#x203A;</div>\n' \
                '</div>'
        else:
            icon_bar_section = ''

        title_text = "Bookmarks" if lang == "en" else "Yer İşaretleri"
        html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title_text}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ 
      background: linear-gradient(135deg, #23272a 0%, #181c20 100%);
      color: #e8eaed; 
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
      min-height: 100vh;
      padding: 20px;
    }}
    .container {{ 
      max-width: 1400px; 
      margin: 0 auto; 
      background: rgba(35, 39, 42, 0.97);
      border-radius: 20px; 
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
      padding: 25px 30px; 
      backdrop-filter: blur(10px);
    }}
    .icon-bar-wrapper {{
      display: flex;
      justify-content: center;
      width: 100%;
      position: relative;
      padding: 0 24px;
      opacity: 0;
      transition: opacity 0.04s;
    }}
    .icon-bar-arrow {{
      display: none;
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      z-index: 2;
      background: rgba(35,39,42,0.92);
      color: #8ab4f8;
      font-size: 1.3em;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      user-select: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.10);
      transition: background 0.18s, color 0.18s, box-shadow 0.18s;
      opacity: 0.93;
      border: 2px solid #23272a;
      outline: none;
    }}
    .icon-bar-arrow:active,
    .icon-bar-arrow:hover {{
      background: #8ab4f8;
      color: #23272a;
      box-shadow: 0 4px 16px #8ab4f8aa;
      border-color: #8ab4f8;
    }}
    .icon-bar-arrow.left {{ left: -18px; margin-left: 0; }}
    .icon-bar-arrow.right {{ right: -18px; margin-right: 0; }}
    .icon-bar {{
      display: flex;
      flex-wrap: nowrap;
      overflow-x: auto;
      gap: 16px;
      justify-content: flex-start;
      align-items: center;
      margin-bottom: 32px;
      padding: 8px 0 18px 0;
      scrollbar-width: thin;
      scrollbar-color: #8ab4f8 #23272a;
      white-space: nowrap;
      max-width: 100%;
      height: 90px;
      padding-left: 12px;
      padding-right: 12px;
    }}
    .icon-bar-item {{
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(42, 59, 92, 0.22);
      box-shadow: 0 2px 8px rgba(0,0,0,0.10);
      border: 1.5px solid rgba(255,255,255,0.07);
      transition: background 0.18s, box-shadow 0.18s, width 0.18s, height 0.18s;
      margin: 0;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .icon-bar-item:hover {{
      width: 53px;
      height: 53px;
      background: rgba(138, 180, 248, 0.18);
      box-shadow: 0 4px 18px rgba(138, 180, 248, 0.18);
    }}
    .icon-bar-favicon {{
      width: 27px;
      height: 27px;
      border-radius: 50%;
      background: #222;
      box-shadow: 0 1px 4px rgba(0,0,0,0.10);
      transition: width 0.18s, height 0.18s, box-shadow 0.18s, transform 0.18s;
    }}
    .icon-bar-item:hover .icon-bar-favicon {{
      width: 32px;
      height: 32px;
    }}
    h1 {{ 
      text-align: center; 
      font-weight: 600; 
      margin-bottom: 40px; 
      letter-spacing: 1px;
      font-size: 2.5em;
      background: none;
      color: #aecbfa;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 18px;
    }}
    .header-title {{
      background: none;
      color: #aecbfa;
      font-family: inherit;
      font-weight: 600;
      font-size: 1em;
      letter-spacing: 1px;
      margin: 0 10px;
      transition: color 0.3s, background 0.3s, text-shadow 0.3s;
      position: relative;
      z-index: 1;
    }}
    .header-title:hover {{
      background: linear-gradient(92deg, #ffe066 0%, #ffd700 40%, #fffbe6 60%, #ffd700 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 0 2px 16px #ffd70088, 0 0px 2px #fffbe6cc;
      animation: goldshine 1.2s linear 1;
    }}
    .header-icon {{
      font-size: 1.2em;
      margin: 0 8px;
      filter: none;
      color: #f7c873;
      text-shadow: 0 2px 8px #23272a44;
      transition: transform 0.18s;
    }}
    .header-icon:first-child,
    .header-icon:nth-child(2) {{
      color: #8ab4f8;
      text-shadow: 0 2px 8px #8ab4f8aa;
    }}
    .header-icon:last-child,
    .header-icon:nth-last-child(2) {{
      color: #f7c873;
      text-shadow: 0 2px 8px #f7c87388;
    }}
    .header-icon:hover {{
      transform: scale(1.18) rotate(-8deg);
      filter: brightness(1.2);
    }}
    .header-icon.sword {{
      position: relative;
      z-index: 1;
      transition: transform 0.25s cubic-bezier(.4,2,.6,1);
    }}
    .header-icon.sword:hover {{
      transform: scale(1.25) rotate(-25deg);
    }}
    .header-icon.sword::after {{
      content: '⚔️';
      position: absolute;
      left: 7px;
      top: 7px;
      opacity: 0;
      font-size: 1.2em;
      filter: blur(0.5px) brightness(1.5);
      pointer-events: none;
      transition: opacity 0.22s, left 0.22s, top 0.22s, filter 0.22s;
      z-index: 0;
    }}
    .header-icon.sword:hover::after {{
      opacity: 0.55;
      left: 0.5em;
      top: 0.5em;
      filter: blur(1.5px) brightness(2.2);
    }}
    .header-icon.crown:hover {{
      transform: scale(1.22) rotate(-12deg) translateY(-8px);
      filter: brightness(1.7) drop-shadow(0 0 8px #f7c87388);
      text-shadow: 0 4px 18px #f7c873cc;
    }}
    .header-icon.left:hover {{
      transform: scale(1.18) rotate(18deg);
    }}
    .header-icon.right:hover {{
      transform: scale(1.18) rotate(-18deg);
    }}
    .bookmarks-grid {{
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 30px;
      margin-top: 0;
    }}
    .bookmarks-grid.only-folders {{
      grid-template-columns: 1fr;
      justify-items: center;
    }}
    .bookmarks-grid.only-root {{
      grid-template-columns: 1fr;
      justify-items: center;
    }}
    .bookmarks-grid.only-folders .right-column {{
      display: none !important;
    }}
    .bookmarks-grid.only-root .left-column {{
      display: none !important;
    }}
    .bookmarks-grid.only-folders .left-column,
    .bookmarks-grid.only-root .right-column {{
      justify-self: center;
      width: 100%;
      max-width: 700px;
    }}
    .left-column {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .right-column {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 20px;
    }}
    details {{ 
      background: rgba(32, 34, 37, 0.92); 
      border-radius: 15px; 
      padding: 0 0 10px 0; 
      box-shadow: 0 8px 25px rgba(0,0,0,0.18);
      border: 1px solid rgba(255,255,255,0.08);
      transition: all 0.3s cubic-bezier(.4,2,.6,1);
      height: fit-content;
      overflow: hidden;
      margin-bottom: 0;
    }}
    .left-column details {{
      width: 100%;
    }}
    .right-column details {{
      display: contents;
    }}
    .right-column details > summary {{
      display: none;
    }}
    .right-column .bookmark-list {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 15px;
      padding: 0;
      margin: 0;
    }}
    .right-column .bookmark-card {{
      flex: none;
      min-width: 0;
    }}
    .folder-icon {{ 
      width: 28px; 
      height: 28px; 
      filter: brightness(0.9);
      transition: transform 0.2s;
    }}
    details[open] .folder-icon {{
      transform: rotate(90deg);
    }}
    .bookmark-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px 18px;
      padding: 18px 18px 10px 18px;
      margin: 0;
      justify-content: flex-start;
      align-items: flex-start;
      background: none;
      border-radius: 0 0 12px 12px;
      min-height: 0;
    }}
    .bookmark-card {{
      flex: 1 1 320px;
      min-width: 220px;
      max-width: 100%;
      background: rgba(42, 59, 92, 0.18);
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: box-shadow 0.2s, background 0.2s, transform 0.15s;
      border: 1px solid rgba(255,255,255,0.04);
      margin: 0;
      padding: 0;
      overflow: hidden;
      display: flex;
      align-items: stretch;
      height: 48px;
    }}
    .bookmark-card a {{
      display: flex;
      align-items: center;
      gap: 14px;
      width: 100%;
      height: 100%;
      padding: 0 18px;
      color: #8ab4f8;
      text-decoration: none;
      font-weight: 500;
      border-radius: 10px;
      transition: background 0.18s, color 0.18s, box-shadow 0.18s, transform 0.15s;
      font-size: 1em;
      line-height: 1.4;
      cursor: pointer;
    }}
    .bookmark-card:hover, .bookmark-card a:hover {{
      background: rgba(42, 59, 92, 0.32);
      color: #fff;
      box-shadow: 0 4px 18px rgba(138, 180, 248, 0.10);
      transform: translateY(-2px) scale(1.03);
    }}
    .bookmark-title {{
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .favicon {{ 
      width: 24px; 
      height: 24px; 
      border-radius: 6px; 
      background: #333; 
      flex-shrink: 0;
      box-shadow: 0 1px 4px rgba(0,0,0,0.10);
      transition: box-shadow 0.18s, transform 0.18s;
    }}
    .bookmark-card:hover .favicon, .bookmark-card a:hover .favicon {{
      box-shadow: 0 2px 8px rgba(138, 180, 248, 0.18);
      transform: scale(1.12);
    }}
    summary {{ 
      font-size: 1.2em; 
      font-weight: 600; 
      cursor: pointer; 
      display: flex; 
      align-items: center; 
      gap: 15px; 
      outline: none; 
      user-select: none;
      padding: 18px 24px 12px 24px;
      transition: color 0.2s;
      color: #8ab4f8;
    }}
    summary:hover {{
      color: #fff;
    }}
    .copyright {{
      text-align: center;
      margin-top: 60px;
      margin-bottom: 18px;
      padding: 22px 0 10px 0;
      color: #8ab4f8;
      font-size: 1.08em;
      opacity: 0.93;
      background: linear-gradient(90deg, #23272a 60%, #181c20 100%);
      border-radius: 18px;
      box-shadow: 0 4px 24px rgba(138,180,248,0.10);
      border: 1.5px solid rgba(138,180,248,0.10);
      letter-spacing: 0.5px;
      transition: background 0.2s;
    }}
    .copyright a {{
      color: #8ab4f8;
      text-decoration: underline;
      font-weight: 600;
      transition: color 0.2s;
    }}
    .copyright a:hover {{
      color: #aecbfa;
      text-shadow: 0 2px 8px #8ab4f8;
    }}
    .header-title.header-title-top {{
      display: block;
      background: none;
      color: #aecbfa;
      transition: color 0.3s, background 0.3s, text-shadow 0.3s;
    }}
    .header-title.header-title-top:hover {{
      background: linear-gradient(92deg, #ffe066 0%, #ffd700 40%, #fffbe6 60%, #ffd700 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 0 2px 16px #ffd70088, 0 0px 2px #fffbe6cc;
      animation: goldshine 1.2s linear 1;
    }}
    .header-title.header-title-bottom {{
      display: block;
      background: none;
      color: #aecbfa;
      transition: color 0.3s, background 0.3s, text-shadow 0.3s;
    }}
    .header-title.header-title-bottom:hover {{
      background: linear-gradient(92deg, #e0e0e0 0%, #b0b0b0 30%, #f8f8f8 60%, #b0b0b0 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 0 2px 16px #b0b0b088, 0 0px 2px #fff;
      animation: silvershine 1.2s linear 1;
    }}
    @keyframes silvershine {{
      0% {{ filter: brightness(1.1); }}
      30% {{ filter: brightness(1.5) drop-shadow(0 0 8px #e0e0e0); }}
      60% {{ filter: brightness(1.8) drop-shadow(0 0 18px #b0b0b0); }}
      100% {{ filter: brightness(1.1); }}
    }}
    .header-icons-row {{
      display: flex;
      justify-content: center;
      gap: 10px;
      margin: 0;
      padding: 0;
    }}
    @media (max-width: 768px) {{ 
      .container {{ 
        padding: 10px 2px; 
        margin: 4px;
      }} 
      h1 {{
        flex-direction: column;
        gap: 0;
        font-size: 1.3em;
      }}
      .header-title {{
        margin: 6px 0 6px 0;
        font-size: 1.3em;
      }}
      .header-icons-row {{
        display: flex;
        justify-content: center;
        gap: 28px;
        margin: 0;
        padding: 0;
      }}
      .header-icons-row:first-child {{
        margin-bottom: 2px;
      }}
      .header-icons-row:last-child {{
        margin-top: 2px;
      }}
      .header-icon {{
        font-size: 1.7em;
      }}
      .bookmarks-grid {{
        grid-template-columns: 1fr;
        gap: 8px;
      }}
      .bookmarks-grid.only-folders .left-column,
      .bookmarks-grid.only-root .right-column {{
        max-width: 100vw;
      }}
      .right-column {{
        grid-template-columns: 1fr;
      }}
      .bookmark-card {{
        min-width: 0;
        max-width: 100%;
      }}
      .bookmark-title {{
        max-width: 120px;
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }}
      .icon-bar-arrow {{ display: flex; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    {icon_bar_section}
    <h1>
      <div class="header-icons-row">
        <span class="header-icon sword left">⚔️</span>
        <span class="header-icon crown left">👑</span>
      </div>
      <span class="header-title header-title-top">{escape(user_name)}</span>
      <span class="header-title header-title-bottom">{'BOOKMARKS' if lang == 'en' else 'YER İŞARETLERİ'}</span>
      <div class="header-icons-row">
        <span class="header-icon sword right">⚔️</span>
        <span class="header-icon crown right">👑</span>
      </div>
    </h1>
    <div class="bookmarks-grid {grid_class}">
      <div class="left-column">{left_html}</div>
      <div class="right-column"><ul class="bookmark-list">{right_html}</ul></div>
    </div>
    <div class="copyright">
      <p>© <span id="copyright-year"></span> {escape(user_name)}</p>
    </div>
  </div>
  
  <script>
    document.querySelectorAll('details').forEach(detail => {{
      detail.addEventListener('toggle', function() {{
        if (this.open) {{
          this.style.background = 'rgba(42, 59, 92, 0.2)';
        }} else {{
          this.style.background = 'rgba(32, 34, 37, 0.8)';
        }}
      }});
    }});
    
    document.getElementById('copyright-year').textContent = new Date().getFullYear();
    // Mobilde oklara tıklayınca ikon barı kaydır
    document.querySelectorAll('.icon-bar-arrow').forEach(function(arrow) {{
      arrow.addEventListener('click', function() {{
        var bar = document.querySelector('.icon-bar');
        if (!bar) return;
        var scrollAmount = 80; // px
        if (arrow.classList.contains('left')) {{
          bar.scrollBy({{ left: -scrollAmount, behavior: 'smooth' }});
        }} else {{
          bar.scrollBy({{ left: scrollAmount, behavior: 'smooth' }});
        }}
      }});
    }});
    // Oklar sadece taşma varsa gözüksün
    function updateIconBarArrows() {{
      var bar = document.querySelector('.icon-bar');
      var leftArrow = document.querySelector('.icon-bar-arrow.left');
      var rightArrow = document.querySelector('.icon-bar-arrow.right');
      if (!bar || !leftArrow || !rightArrow) return;
      if (window.innerWidth > 768) {{
        leftArrow.style.display = 'none';
        rightArrow.style.display = 'none';
        return;
      }}
      if (bar.scrollWidth > bar.clientWidth + 2) {{
        leftArrow.style.display = 'flex';
        rightArrow.style.display = 'flex';
      }} else {{
        leftArrow.style.display = 'none';
        rightArrow.style.display = 'none';
      }}
    }}
    window.addEventListener('resize', updateIconBarArrows);
    window.addEventListener('DOMContentLoaded', function() {{
      setTimeout(function() {{
        updateIconBarArrows();
        var wrapper = document.querySelector('.icon-bar-wrapper');
        if (wrapper) wrapper.style.opacity = '1';
      }}, 120);
    }});
    // Faviconlar yüklenince okları tekrar kontrol et
    document.querySelectorAll('.icon-bar-favicon').forEach(function(img) {{
      img.addEventListener('load', updateIconBarArrows);
      img.addEventListener('error', updateIconBarArrows);
    }});
  </script>
</body>
</html>'''
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return False

def sort_bookmarks_html(input_file, output_file):
    """
    input_file'daki <DL> içeriğini önce klasörler (DT > H3 + DL), sonra kök yer imleri (DT > A) olacak şekilde sıralar.
    Sıralanmış yeni bir HTML dosyasını output_file olarak kaydeder.
    """
    from bs4 import BeautifulSoup
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    dl = soup.find('dl')
    if not dl:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return
    
    # Dosyayı kaydet
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

import os
from flask import Flask, render_template_string, redirect, request

app = Flask(__name__)

# Đường dẫn đến thư mục data (Vercel sẽ mount thư mục này từ GitHub)
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def get_file_tree():
    files_info = []
    if os.path.exists(DATA_DIR):
        # Lấy danh sách tất cả file .txt trong thư mục data
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        for filename in files:
            path = os.path.join(DATA_DIR, filename)
            with open(path, 'r', encoding='utf-8') as f:
                # Đọc dòng đầu tiên làm tiêu đề hiển thị trên nút
                title = f.readline().strip()
                files_info.append({
                    'slug': filename.replace('.txt', ''),
                    'title': title
                })
    return files_info

@app.route('/')
def index():
    files = get_file_tree()
    
    # CSS tạo giao diện danh sách nút bấm chuyên nghiệp
    style = """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 40px; color: #333; }
        .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 15px; shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #1a73e8; }
        .file-list { margin-top: 20px; }
        .file-item { 
            display: flex; align-items: center; 
            padding: 15px; margin-bottom: 10px; 
            background: #fff; border: 1px solid #ddd; 
            border-radius: 8px; text-decoration: none; 
            color: #333; transition: all 0.2s; 
        }
        .file-item:hover { background: #e8f0fe; border-color: #1a73e8; transform: translateX(5px); }
        .icon { margin-right: 15px; font-size: 20px; }
    </style>
    """
    
    # Tạo danh sách các nút từ file
    items_html = ""
    for file in files:
        items_html += f'''
        <a href="/view/{file['slug']}" class="file-item">
            <span class="icon">📄</span>
            <span>{file['title']}</span>
        </a>
        '''
        
    html = f"""
    <html>
        <head><title>Hệ thống Tài liệu</title>{style}</head>
        <body>
            <div class="container">
                <h1>📚 Danh mục Tài liệu</h1>
                <div class="file-list">{items_html}</div>
            </div>
        </body>
    </html>
    """
    return render_template_string(html)

@app.route('/view/<slug>')
def view_file(slug):
    file_path = os.path.join(DATA_DIR, f"{slug}.txt")
    if not os.path.exists(file_path):
        return "File không tồn tại", 404
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        title = lines[0].strip()   # Dòng 1: Tiêu đề
        ads_url = lines[1].strip() # Dòng 2: Link quảng cáo
        content = "".join(lines[2:]) # Còn lại là nội dung
        
    # Giao diện trang nội dung
    html = f"""
    <html>
        <body style="max-width:800px; margin:auto; padding:50px; line-height:1.6; font-family:serif;">
            <h1>{title}</h1>
            <div style="white-space: pre-wrap;">{content}</div>
            <hr>
            <div style="text-align:center; margin-top:30px;">
                <a href="{ads_url}" style="background:#28a745; color:white; padding:15px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
                    CLICK ĐỂ TẢI XUỐNG BẢN FULL (.PDF)
                </a>
            </div>
        </body>
    </html>
    """
    return render_template_string(html)

def handler(event, context):
    return app(event, context)

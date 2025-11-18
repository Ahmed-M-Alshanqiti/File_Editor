# File Editor

A comprehensive Django-based web application for viewing, editing, and managing various file types including PDFs, text files, images, and documents.

## 🌟 Features

- **Multi-Format Support**: Handle PDF, TXT, DOCX, images, and more
- **PDF Viewer**: Integrated PDF.js for seamless PDF viewing and navigation
- **Text Editor**: Edit text-based files with rich editing capabilities
- **File Management**: Upload, download, rename, and organize files
- **User Authentication**: Secure user accounts and file access
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Static File Handling**: Optimized serving of CSS, JavaScript, and media files

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Static Files & PDF.js Setup](#static-files--pdfjs-setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Dependencies](#dependencies)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)
- Git (for cloning the repository)

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmed-M-Alshanqiti/File_Editor.git
cd File_Editor
```

### 2. Create and Activate Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```



### 5. Set Up Static Files

Ensure the static files directory structure exists:

```bash
mkdir -p static/css static/js static/pdf.js static/uploads
mkdir -p media/uploads
```

## 📁 Project Structure

```
File_Editor/
│
├── core/                          # Django project folder
│   ├── core/                      # Main settings folder
│   │   ├── __init__.py
│   │   ├── settings.py            # Main settings file
│   │   ├── urls.py                # Root URL configuration
│   │   ├── wsgi.py                # WSGI configuration
│   │   └── asgi.py                # ASGI configuration
│   │
│   ├── apps/                      # Django applications
│   │   ├── editor/                # File editor app
│   │   ├── accounts/              # User authentication
│   │   └── __init__.py
│   │
│   ├── static/                    # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── app.js
│   │   ├── pdf.js/                # PDF.js library
│   │   │   ├── pdf.js
│   │   │   ├── pdf.worker.js
│   │   │   ├── viewer.html
│   │   │   └── viewer.css
│   │   └── uploads/               # Temporary static uploads
│   │
│   ├── media/                     # User uploaded files
│   │   └── uploads/
│   │
│   ├── templates/                 # HTML templates
│   │   ├── base.html
│   │   ├── editor/
│   │   └── accounts/
│   │
│   └── manage.py                  # Django management script
│
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (not in repo)
├── .gitignore
└── README.md                     # This file
```

## ⚙️ Configuration

### Django Settings (core/core/settings.py)

The main configuration file located at `core/core/settings.py` contains all Django settings.

#### Important Settings:

**Secret Key:**
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
```

**Debug Mode:**
```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

**Allowed Hosts:**
```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

**Installed Apps:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your apps
    'apps.editor',
    'apps.accounts',
]
```

**Static Files Configuration:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**File Upload Settings:**
```python
# Maximum upload size: 100MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600
```

## 📚 Static Files & PDF.js Setup

### Installing PDF.js

1. **Download PDF.js:**

```bash
cd static
mkdir pdf.js
cd pdf.js

# Download from CDN or official release
wget https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js -O pdf.js
wget https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js -O pdf.worker.js
```

Or download the full package from: https://github.com/mozilla/pdf.js/releases

2. **Required PDF.js Files:**
   - `pdf.js` - Core PDF.js library
   - `pdf.worker.js` - Web Worker for rendering
   - `viewer.html` - PDF viewer interface (optional)
   - `viewer.css` - Viewer styles (optional)

### Using PDF.js in Django Templates

```django
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <title>PDF Viewer</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <canvas id="pdf-canvas"></canvas>
    
    <script src="{% static 'pdf.js/pdf.js' %}"></script>
    <script>
        // Configure PDF.js worker
        pdfjsLib.GlobalWorkerOptions.workerSrc = "{% static 'pdf.js/pdf.worker.js' %}";
        
        // Load and render PDF
        const url = "{% static 'uploads/sample.pdf' %}";
        pdfjsLib.getDocument(url).promise.then(function(pdf) {
            pdf.getPage(1).then(function(page) {
                const canvas = document.getElementById('pdf-canvas');
                const context = canvas.getContext('2d');
                const viewport = page.getViewport({ scale: 1.5 });
                
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                
                page.render({
                    canvasContext: context,
                    viewport: viewport
                });
            });
        });
    </script>
</body>
</html>
```

### Serving Static Files in Development

In `core/core/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.editor.urls')),
    path('accounts/', include('apps.accounts.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Collecting Static Files for Production

```bash
python manage.py collectstatic
```

## 🗄️ Database Setup

### Using SQLite (Default)

No additional setup required. Django will create `db.sqlite3` automatically.






### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

## 🚀 Running the Application

### Development Server

```bash
# Navigate to core directory
cd core

# Run development server
python manage.py runserver

# Or specify host and port
python manage.py runserver 0.0.0.0:8000
```

Access the application at: `http://localhost:8000`

Admin panel: `http://localhost:8000/admin`

### Running with Gunicorn (Production)

```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 📦 Dependencies

Create `requirements.txt` with:

```txt
Django==4.2.7
Pillow==10.1.0
PyPDF2==3.0.1
python-dotenv==1.0.0
python-docx==1.1.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

## 🔌 API Endpoints

### File Management

```
GET  /                          - Home page
GET  /files/                    - List all files
POST /files/upload/             - Upload file
GET  /files/view/<int:id>/      - View file
GET  /files/edit/<int:id>/      - Edit file
POST /files/save/<int:id>/      - Save changes
GET  /files/download/<int:id>/  - Download file
DELETE /files/delete/<int:id>/  - Delete file
POST /files/rename/<int:id>/    - Rename file
```




## 👤 Author

**Ahmed M. Alshanqiti**

- GitHub: [@Ahmed-M-Alshanqiti](https://github.com/Ahmed-M-Alshanqiti)
- Repository: [File_Editor](https://github.com/Ahmed-M-Alshanqiti/File_Editor)


---

**Quick Start Commands:**

```bash
# Clone and setup
git clone https://github.com/Ahmed-M-Alshanqiti/File_Editor.git
cd File_Editor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup database
cd core
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to start using the application!

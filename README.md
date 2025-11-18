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

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL)
DB_NAME=file_editor_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
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

### Using PostgreSQL (Recommended for Production)

1. **Install PostgreSQL and create database:**

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE file_editor_db;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE file_editor_db TO your_user;
\q
```

2. **Update settings.py:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'file_editor_db'),
        'USER': os.environ.get('DB_USER', 'your_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

3. **Install PostgreSQL adapter:**

```bash
pip install psycopg2-binary
```

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

### User Authentication

```
GET  /accounts/login/           - Login page
POST /accounts/login/           - Login submission
GET  /accounts/register/        - Registration page
POST /accounts/register/        - Registration submission
GET  /accounts/logout/          - Logout
GET  /accounts/profile/         - User profile
```

## 🐛 Troubleshooting

### Common Issues

**1. PDF.js not loading:**

```
Error: Cannot find pdf.worker.js

Solution: Ensure pdf.worker.js path is correctly set:
pdfjsLib.GlobalWorkerOptions.workerSrc = "{% static 'pdf.js/pdf.worker.js' %}";
```

**2. Static files not found (404):**

```
Solution: 
1. Run: python manage.py collectstatic
2. Check STATIC_URL and STATIC_ROOT in settings.py
3. Ensure static files are in correct directory
4. In development, set DEBUG=True
```

**3. File upload fails:**

```
Solution:
1. Check DATA_UPLOAD_MAX_MEMORY_SIZE in settings.py
2. Ensure MEDIA_ROOT directory exists and has write permissions
3. Check disk space
```

**4. Database migration errors:**

```
Solution:
1. Delete all migration files except __init__.py
2. Delete db.sqlite3
3. Run: python manage.py makemigrations
4. Run: python manage.py migrate
```

**5. Permission denied on media folder:**

```bash
# Linux/Mac
sudo chmod -R 755 media/
sudo chown -R $USER:$USER media/

# Windows - Run as Administrator
icacls media /grant Everyone:F /T
```

### Debug Mode

Enable detailed error messages in development:

```python
# settings.py
DEBUG = True
ALLOWED_HOSTS = ['*']  # Only for development!
```

## 🚢 Deployment

### Preparing for Production

1. **Update settings.py:**

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
```

2. **Install WhiteNoise for static files:**

```bash
pip install whitenoise
```

Add to `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

3. **Collect static files:**

```bash
python manage.py collectstatic --noinput
```

4. **Security settings:**

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### Deployment Options

- **Heroku**: Use Procfile and configure buildpacks
- **AWS**: Use Elastic Beanstalk or EC2 with nginx
- **DigitalOcean**: Deploy on App Platform or Droplet
- **Railway**: Simple deployment with GitHub integration

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

### Coding Standards

- Follow PEP 8 style guide for Python code
- Use Django best practices
- Write docstrings for functions and classes
- Add comments for complex logic
- Write unit tests for new features

### Running Tests

```bash
python manage.py test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ahmed M. Alshanqiti**

- GitHub: [@Ahmed-M-Alshanqiti](https://github.com/Ahmed-M-Alshanqiti)
- Repository: [File_Editor](https://github.com/Ahmed-M-Alshanqiti/File_Editor)

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines
- [PDF.js](https://mozilla.github.io/pdf.js/) - Mozilla's PDF rendering library
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- The Django community for excellent documentation and support

## 📞 Support

For issues, questions, or contributions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search [existing issues](https://github.com/Ahmed-M-Alshanqiti/File_Editor/issues)
3. Open a new issue with detailed information

## 🔐 Security

If you discover a security vulnerability, please email directly instead of using the issue tracker.

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

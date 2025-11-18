# files/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('<int:pk>/', views.file_detail, name='file_detail'),
    path('<int:file_id>/edit/', views.file_edit, name='file_edit'),
    path('<int:pk>/delete/', views.file_delete, name='file_delete'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/convert/', views.convert_to_pdf, name='convert_to_pdf'),
    path('<int:pk>/original/', views.download_original, name='download_original'),
    path('<int:pk>/view-pdf/', views.view_pdf, name='view_pdf'),  # ✅ NEW: For PDF.js viewer
    path('<int:pk>/download-pdf/', views.download_pdf, name='download_pdf'),  # ✅ Renamed for clarity
    path('<int:pk>/status/<str:action>/', views.update_file_status, name='update_file_status'),
    path('notifications/', views.notifications_list, name='notifications'),
]
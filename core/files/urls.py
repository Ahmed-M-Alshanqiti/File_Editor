from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('convert/<int:file_id>/', views.convert_to_pdf, name='convert_to_pdf'),
]

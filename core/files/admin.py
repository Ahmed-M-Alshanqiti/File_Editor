from django.contrib import admin
from .models import UploadedFile, Comment

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'owner', 'uploaded_at', 'file_name_if_converted')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'created_at')

# files/models
from django.db import models
import os
from decimal import Decimal
from django.contrib.auth.models import User


class FileStatus(models.TextChoices):
    PENDING = ('pending', 'Pending')
    IN_REVIEW = ('in_review', 'In review')
    APPROVED = ('approved', 'Approved')
    REJECTED = ('rejected', 'Rejected')


class ChangeTypes(models.TextChoices):
    MINOR = ('minor', 'Minor (+0.1)')
    MAJOR = ('major', 'Major (+1.0)')


class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted = models.FileField(upload_to="converted/", blank=True, null=True)
    file_name_if_converted = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=FileStatus.choices, default=FileStatus.PENDING)
    version_number = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('1.0'))
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviewed_files')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    # owner: who uploaded this file
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='uploaded_files')

    def save(self, *args, **kwargs):
        if self.file and not self.filename:
            self.filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove file and converted file from disk if they exist
        try:
            if self.file and os.path.isfile(self.file.path):
                os.remove(self.file.path)
        except Exception:
            pass
        try:
            if self.converted and os.path.isfile(self.converted.path):
                os.remove(self.converted.path)
        except Exception:
            pass
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.filename or "Unnamed File"

    def bump_version(self, change_type):
        if change_type == ChangeTypes.MAJOR:
            self.version_number = (self.version_number or Decimal('0')) + Decimal('1.0')
        else:
            self.version_number = (self.version_number or Decimal('0')) + Decimal('0.1')
        # Normalize to one decimal place
        self.version_number = self.version_number.quantize(Decimal('0.1'))
        return self.version_number

    @property
    def version_label(self):
        return f"{self.version_number:.1f}"


class UploadedFileVersion(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='versions')
    version_label = models.CharField(max_length=10)
    change_type = models.CharField(max_length=10, choices=ChangeTypes.choices)
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file} v{self.version_label}"


class Comment(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else 'Anon'
        return f"Comment by {username} on {self.file}"


class Notification(models.Model):
    class Types(models.TextChoices):
        FILE_SUBMITTED = ('file_submitted', 'File submitted')
        FILE_APPROVED = ('file_approved', 'File approved')
        FILE_REJECTED = ('file_rejected', 'File rejected')
        GENERAL = ('general', 'General')

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    notification_type = models.CharField(max_length=40, choices=Types.choices)
    message = models.TextField()
    related_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.recipient} - {self.notification_type}"

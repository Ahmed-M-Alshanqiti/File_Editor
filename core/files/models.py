from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.name
        super().save(*args, **kwargs)

from django.db import models


class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to='images/')
    filtered_image = models.ImageField(upload_to='filtered_images/')
    filter_used = models.CharField(max_length=50)
    processed_at = models.DateTimeField(auto_now_add=True)
    image_name = models.CharField(max_length=255)
    processed_successfully = models.BooleanField(default=False)

    def __str__(self):
        return f"Processed Image {self.id}"

from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)  # optional image
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields for downloads and payments
    download_url = models.URLField(blank=True, null=True)  # public free download link
    file_path = models.CharField(max_length=500, blank=True, null=True)  # internal path for protected file
    requires_payment = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    demo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

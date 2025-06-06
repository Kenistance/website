# backend/portfolio/models.py
from django.db import models

class Project(models.Model):
    # Choices for the new project_type field
    PROJECT_TYPE_CHOICES = [
        ('program', 'Program'),  # A software/application that can be downloaded (paid or free)
        ('website', 'Website'),  # A web project that has a live URL
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    # Keep image_url as per your existing model and frontend's project.image
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Core fields for downloads and payments, now clarified by project_type
    download_url = models.URLField(blank=True, null=True, help_text="Public URL for free program downloads.")
    file_path = models.CharField(max_length=500, blank=True, null=True, help_text="Internal path for protected program files.")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Price for paid programs/projects. Set to 0 for free.")
    demo_url = models.URLField(blank=True, null=True, help_text="URL for a demo or preview of the project.")

    # New fields to categorize and link projects
    project_type = models.CharField(
        max_length=20,
        choices=PROJECT_TYPE_CHOICES,
        default='program', # Sensible default if not explicitly set
        help_text="Defines if the project is a 'program' (downloadable/paid) or a 'website' (link)."
    )
    website_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="The live URL for 'website' type projects."
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at'] # Ensures latest projects appear first
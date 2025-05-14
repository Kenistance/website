from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)  # optional image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

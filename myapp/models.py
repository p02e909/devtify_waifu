from django.db import models

class Photo(models.Model):
    url = models.URLField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
        
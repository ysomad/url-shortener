from django.db import models
from django.utils.crypto import get_random_string


class URL(models.Model):
    original_url = models.URLField(
        max_length=2048,
        verbose_name='original URL'
    )
    code = models.CharField(
        max_length=16, 
        default=get_random_string, 
        unique=True,
        verbose_name='unique code'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='timestamp'
    )
    
    class Meta:
        db_table = 'shortened_urls'

    def __str__(self):
        return self.code


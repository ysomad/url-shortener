from loguru import logger

from django.db import models
from django.utils.crypto import get_random_string


class URL(models.Model):
    original_url = models.URLField(
        max_length=2048,
        verbose_name='original URL'
    )
    code = models.CharField(
        max_length=16, 
        unique=True,
        blank=True,
        verbose_name='unique code'
    )
    session = models.CharField(
        max_length=256, 
        blank=True, 
        null=True,
        verbose_name='session id')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='timestamp'
    )
    
    class Meta:
        db_table = 'shortened_urls'
        ordering = ('-created_at',)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        """При сохранении модели, создает уникальный код для
        укороченного URLа и сохраняет в кэш"""
        if not self.code:
            self.code = get_random_string(length=4)

        logger.info((
            f'Original URL "{self.original_url}" saved with '
            f'code "{self.code}" in db for session "{self.session}"'
        ))

        return super().save(*args, **kwargs)


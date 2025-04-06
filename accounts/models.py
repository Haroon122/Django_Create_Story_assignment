from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Statistics
    stories_created = models.PositiveIntegerField(default=0)
    chapters_written = models.PositiveIntegerField(default=0)
    votes_cast = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.username})

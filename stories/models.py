from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

class Story(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    description = models.TextField()
    cover_image = models.ImageField(upload_to='story_covers/', null=True, blank=True)
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'stories'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('stories:story_detail', kwargs={'pk': self.pk})

class Chapter(MPTTModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='chapters')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    content = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    votes_for = models.PositiveIntegerField(default=0)
    votes_against = models.PositiveIntegerField(default=0)
    
    class MPTTMeta:
        order_insertion_by = ['created_at']
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.story.title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('stories:chapter_detail', kwargs={'pk': self.pk})

class Vote(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    is_approve = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['chapter', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} {'approved' if self.is_approve else 'rejected'} {self.chapter.title}"

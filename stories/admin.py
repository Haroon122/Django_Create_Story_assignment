from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Story, Chapter, Vote

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'created_at', 'is_public')
    list_filter = ('genre', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Chapter)
class ChapterAdmin(MPTTModelAdmin):
    list_display = ('title', 'story', 'author', 'status', 'created_at', 'votes_for', 'votes_against')
    list_filter = ('status', 'created_at', 'story')
    search_fields = ('title', 'content', 'author__username', 'story__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    mptt_level_indent = 20

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'is_approve', 'created_at')
    list_filter = ('is_approve', 'created_at')
    search_fields = ('user__username', 'chapter__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

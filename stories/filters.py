import django_filters
from django.db.models import Q
from .models import Story

class StoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Search')
    genre = django_filters.ChoiceFilter(
        choices=[
            ('fantasy', 'Fantasy'),
            ('sci-fi', 'Science Fiction'),
            ('mystery', 'Mystery'),
            ('romance', 'Romance'),
            ('horror', 'Horror'),
            ('adventure', 'Adventure'),
            ('other', 'Other')
        ]
    )
    sort = django_filters.ChoiceFilter(
        choices=[
            ('recent', 'Most Recent'),
            ('popular', 'Most Popular'),
            ('chapters', 'Most Chapters')
        ],
        method='sort_filter',
        label='Sort By',
        empty_label='Sort By'
    )
    
    class Meta:
        model = Story
        fields = ['search', 'genre', 'sort']
    
    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value)
        )
    
    def sort_filter(self, queryset, name, value):
        if value == 'recent':
            return queryset.order_by('-created_at')
        elif value == 'popular':
            return queryset.annotate(
                total_chapters=models.Count('chapters', filter=Q(chapters__status='approved'))
            ).order_by('-total_chapters')
        elif value == 'chapters':
            return queryset.annotate(
                chapter_count=models.Count('chapters')
            ).order_by('-chapter_count')
        return queryset 
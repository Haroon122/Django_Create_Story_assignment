from django import forms
from .models import Story, Chapter

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'description', 'cover_image', 'genre', 'is_public')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'content', 'parent')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'title': 'Give your chapter a descriptive title',
            'content': 'Write the content of your chapter here',
            'parent': 'Select a parent chapter if this is a continuation or alternative path',
        }
    
    def __init__(self, *args, **kwargs):
        story = kwargs.pop('story', None)
        super().__init__(*args, **kwargs)
        if story:
            self.fields['parent'].queryset = Chapter.objects.filter(
                story=story,
                status='approved'
            )
            self.fields['parent'].empty_label = "No parent (start a new branch)"
            self.fields['parent'].label = "Parent Chapter (Optional)" 
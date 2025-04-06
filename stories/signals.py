from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from .models import Vote, Chapter

@receiver(post_save, sender=Vote)
def update_chapter_status(sender, instance, created, **kwargs):
    """
    Signal to update chapter status based on votes.
    A chapter is approved when it has at least 3 approval votes and
    the ratio of approval votes to total votes is at least 0.7 (70%).
    """
    chapter = instance.chapter
    
    # Only process pending chapters
    if chapter.status != 'pending':
        return
    
    # Get vote counts
    total_votes = chapter.votes_for + chapter.votes_against
    
    # Check if the chapter meets approval criteria
    if chapter.votes_for >= 3 and total_votes >= 3 and (chapter.votes_for / total_votes) >= 0.7:
        chapter.status = 'approved'
        chapter.save() 
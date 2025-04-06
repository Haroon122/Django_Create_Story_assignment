from django.core.management.base import BaseCommand
from stories.models import Chapter

class Command(BaseCommand):
    help = 'Approve chapters that meet the approval criteria'

    def handle(self, *args, **options):
        # Get all pending chapters
        pending_chapters = Chapter.objects.filter(status='pending')
        approved_count = 0
        
        for chapter in pending_chapters:
            # Get vote counts
            total_votes = chapter.votes_for + chapter.votes_against
            
            # Check if the chapter meets approval criteria
            if chapter.votes_for >= 3 and total_votes >= 3 and (chapter.votes_for / total_votes) >= 0.7:
                chapter.status = 'approved'
                chapter.save()
                approved_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Approved chapter: {chapter.title} (ID: {chapter.pk})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully approved {approved_count} chapters')
        ) 
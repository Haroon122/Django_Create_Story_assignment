from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q, F
from django_filters.views import FilterView
from .models import Story, Chapter, Vote
from .forms import StoryForm, ChapterForm
from .filters import StoryFilter
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

class StoryListView(FilterView):
    model = Story
    template_name = 'stories/story_list.html'
    context_object_name = 'stories'
    filterset_class = StoryFilter
    paginate_by = 12

class StoryDetailView(DetailView):
    model = Story
    template_name = 'stories/story_detail.html'
    context_object_name = 'story'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story = self.get_object()
        context['chapters'] = story.chapters.filter(status='approved')
        return context

class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'stories/story_form.html'
    success_url = reverse_lazy('stories:story_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        self.request.user.stories_created += 1
        self.request.user.save()
        return super().form_valid(form)

class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = ChapterForm
    template_name = 'stories/chapter_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        story = get_object_or_404(Story, pk=self.kwargs['story_pk'])
        kwargs['story'] = story
        
        # Check if parent chapter is specified in the URL
        parent_pk = self.request.GET.get('parent')
        if parent_pk:
            try:
                parent_chapter = Chapter.objects.get(pk=parent_pk, story=story)
                if parent_chapter.status == 'approved':
                    kwargs['initial'] = {'parent': parent_chapter}
            except Chapter.DoesNotExist:
                pass
                
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story = get_object_or_404(Story, pk=self.kwargs['story_pk'])
        context['story'] = story
        return context
    
    def form_valid(self, form):
        story = get_object_or_404(Story, pk=self.kwargs['story_pk'])
        form.instance.story = story
        form.instance.author = self.request.user
        self.request.user.chapters_written += 1
        self.request.user.save()
        
        response = super().form_valid(form)
        messages.success(self.request, 'Your chapter has been submitted and is pending approval.')
        return response
        
    def get_success_url(self):
        return reverse('stories:story_detail', kwargs={'pk': self.kwargs['story_pk']})

class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'stories/chapter_detail.html'
    context_object_name = 'chapter'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = self.get_object()
        if self.request.user.is_authenticated:
            context['user_vote'] = Vote.objects.filter(
                chapter=chapter,
                user=self.request.user
            ).first()
        return context

@login_required
def vote_chapter(request, pk):
    try:
        chapter = get_object_or_404(Chapter, pk=pk)
        
        # Check if chapter is pending
        if chapter.status != 'pending':
            messages.error(request, 'You can only vote on pending chapters.')
            return redirect('stories:chapter_detail', pk=pk)
            
        # Check if user is the author
        if request.user == chapter.author:
            messages.error(request, 'You cannot vote on your own chapter.')
            return redirect('stories:chapter_detail', pk=pk)
            
        vote_value = request.POST.get('vote')
        if vote_value not in ['approve', 'reject']:
            messages.error(request, 'Invalid vote value.')
            return redirect('stories:chapter_detail', pk=pk)
            
        is_approve = vote_value == 'approve'
        
        try:
            with transaction.atomic():
                # Get existing vote if any
                existing_vote = Vote.objects.filter(
                    chapter=chapter,
                    user=request.user
                ).first()
                
                if existing_vote:
                    # If changing vote from approve to reject or vice versa
                    if existing_vote.is_approve != is_approve:
                        # Update vote counts
                        if existing_vote.is_approve:
                            Chapter.objects.filter(pk=chapter.pk).update(
                                votes_for=F('votes_for') - 1,
                                votes_against=F('votes_against') + 1
                            )
                        else:
                            Chapter.objects.filter(pk=chapter.pk).update(
                                votes_for=F('votes_for') + 1,
                                votes_against=F('votes_against') - 1
                            )
                        
                        # Update the vote
                        existing_vote.is_approve = is_approve
                        existing_vote.save()
                else:
                    # Create a new vote
                    Vote.objects.create(
                        chapter=chapter,
                        user=request.user,
                        is_approve=is_approve
                    )
                    
                    # Update vote counts
                    if is_approve:
                        Chapter.objects.filter(pk=chapter.pk).update(
                            votes_for=F('votes_for') + 1
                        )
                    else:
                        Chapter.objects.filter(pk=chapter.pk).update(
                            votes_against=F('votes_against') + 1
                        )
                    
                    # Update user's votes_cast count using F() expression
                    User = get_user_model()
                    User.objects.filter(pk=request.user.pk).update(
                        votes_cast=F('votes_cast') + 1
                    )
                
                # Refresh both objects to get updated counts
                chapter.refresh_from_db()
                request.user.refresh_from_db()
                
                messages.success(request, 'Vote recorded successfully.')
                
        except IntegrityError:
            messages.error(request, 'Error recording vote: Database integrity error')
            
    except Exception as e:
        messages.error(request, f'Error recording vote: {str(e)}')
        
    return redirect('stories:chapter_detail', pk=pk)

@login_required
def approve_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    
    # Check if user is the author or has staff permissions
    if request.user != chapter.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to approve this chapter.')
        return redirect('stories:chapter_detail', pk=pk)
    
    # Update chapter status
    chapter.status = 'approved'
    chapter.save()
    
    messages.success(request, f'Chapter "{chapter.title}" has been approved.')
    return redirect('stories:chapter_detail', pk=pk)

@login_required
def reject_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    
    # Check if user is the author or has staff permissions
    if request.user != chapter.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to reject this chapter.')
        return redirect('stories:chapter_detail', pk=pk)
    
    # Update chapter status
    chapter.status = 'rejected'
    chapter.save()
    
    messages.success(request, f'Chapter "{chapter.title}" has been rejected.')
    return redirect('stories:chapter_detail', pk=pk)

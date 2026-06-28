from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from .models import Feedback
from .forms import FeedbackForm


@login_required
def leave_feedback(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)

    if request.user.role != 'attendee':
        messages.error(request, 'Only attendees can leave feedback.')
        return redirect('event_detail', pk=event_pk)

    existing = Feedback.objects.filter(event=event, user=request.user).first()
    if existing:
        messages.info(request, 'You have already left feedback for this event.')
        return redirect('event_detail', pk=event_pk)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully.')
            return redirect('event_detail', pk=event_pk)
    else:
        form = FeedbackForm()

    return render(request, 'feedback/leave_feedback.html', {'form': form, 'event': event})


def event_feedback(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    feedback_list = Feedback.objects.filter(event=event).order_by('-created_at')
    avg_rating = sum([f.rating for f in feedback_list]) / len(feedback_list) if feedback_list else 0

    context = {
        'event': event,
        'feedback_list': feedback_list,
        'avg_rating': round(avg_rating, 1),
    }
    return render(request, 'feedback/event_feedback.html', context)
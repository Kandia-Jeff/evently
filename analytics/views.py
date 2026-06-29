from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from events.models import Event
from feedback.models import Feedback
from flagging.models import Flag
from accounts.models import User
from .models import EventView


@login_required
def organiser_analytics_view(request):
    if request.user.role != 'organiser':
        from django.shortcuts import redirect
        return redirect('event_list')

    events = Event.objects.filter(organiser=request.user).annotate(
        view_count=Count('views', distinct=True),
        feedback_count=Count('feedback', distinct=True),
        avg_rating=Avg('feedback__rating')
    ).order_by('-created_at')

    total_views = sum(e.view_count for e in events)
    total_feedback = sum(e.feedback_count for e in events)
    overall_avg = events.aggregate(Avg('feedback__rating'))['feedback__rating__avg']

    context = {
        'events': events,
        'total_views': total_views,
        'total_feedback': total_feedback,
        'overall_avg': round(overall_avg, 1) if overall_avg else 0,
    }
    return render(request, 'analytics/organiser_analytics.html', context)


def admin_analytics_view(request):
    if not request.user.is_staff:
        from django.shortcuts import redirect
        return redirect('event_list')

    total_users = User.objects.count()
    total_attendees = User.objects.filter(role='attendee').count()
    total_organisers = User.objects.filter(role='organiser').count()
    verified_organisers = User.objects.filter(role='organiser', is_verified=True).count()
    total_events = Event.objects.count()
    approved_events = Event.objects.filter(status='approved').count()
    pending_events = Event.objects.filter(status='pending').count()
    rejected_events = Event.objects.filter(status='rejected').count()
    total_feedback = Feedback.objects.count()
    total_flags = Flag.objects.count()
    pending_flags = Flag.objects.filter(fl_status='pending').count()
    total_views = EventView.objects.count()

    top_events = Event.objects.filter(status='approved').annotate(
        view_count=Count('views')
    ).order_by('-view_count')[:5]

    context = {
        'total_users': total_users,
        'total_attendees': total_attendees,
        'total_organisers': total_organisers,
        'verified_organisers': verified_organisers,
        'total_events': total_events,
        'approved_events': approved_events,
        'pending_events': pending_events,
        'rejected_events': rejected_events,
        'total_feedback': total_feedback,
        'total_flags': total_flags,
        'pending_flags': pending_flags,
        'total_views': total_views,
        'top_events': top_events,
    }
    return render(request, 'analytics/admin_analytics.html', context)
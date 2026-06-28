from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from events.models import Event
from .models import Flag
from .forms import FlagForm


@login_required
def flag_event(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)

    existing = Flag.objects.filter(event=event, user=request.user).first()
    if existing:
        messages.info(request, 'You have already flagged this event.')
        return redirect('event_detail', pk=event_pk)

    if request.method == 'POST':
        form = FlagForm(request.POST)
        if form.is_valid():
            flag = form.save(commit=False)
            flag.event = event
            flag.user = request.user
            flag.save()
            messages.success(request, 'Event flagged successfully. Admin will review it.')
            return redirect('event_detail', pk=event_pk)
    else:
        form = FlagForm()

    return render(request, 'flagging/flag_event.html', {'form': form, 'event': event})


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def flag_list(request):
    flags = Flag.objects.all().order_by('-created_at')
    return render(request, 'flagging/flag_list.html', {'flags': flags})


@user_passes_test(is_admin)
def review_flag(request, flag_pk):
    flag = get_object_or_404(Flag, pk=flag_pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            flag.fl_status = 'approved'
            flag.save()
            flag.event.status = 'cancelled'
            flag.event.save()
            messages.success(request, 'Flag approved. Event has been cancelled.')
        elif action == 'reject':
            flag.fl_status = 'rejected'
            flag.save()
            messages.success(request, 'Flag rejected.')
        return redirect('flag_list')

    return render(request, 'flagging/review_flag.html', {'flag': flag})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventUpdate
from .forms import EventForm, EventUpdateForm


def event_list_view(request):
    events = Event.objects.filter(status='approved').order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail_view(request, pk):
    from django.db.models import Q
    from analytics.models import EventView

    event = get_object_or_404(
        Event,
        Q(status='approved') | Q(organiser=request.user) if request.user.is_authenticated else Q(status='approved'),
        pk=pk
    )

    # Record a view
    EventView.objects.create(event=event)

    updates = event.updates.order_by('-created_at')
    return render(request, 'events/event_detail.html', {'event': event, 'updates': updates})


@login_required
def event_create_view(request):
    if request.user.role != 'organiser':
        messages.error(request, 'Only organisers can create events.')
        return redirect('event_list')

    if not request.user.is_verified:
        messages.error(request, 'You must be verified before creating events.')
        return redirect('verification_status')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organiser = request.user
            event.save()
            messages.success(request, 'Event submitted for admin review.')
            return redirect('organiser_dashboard')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})


@login_required
def event_edit_view(request, pk):
    event = get_object_or_404(Event, pk=pk, organiser=request.user)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event updated and resubmitted for review.')
            return redirect('organiser_dashboard')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Edit'})


@login_required
def event_delete_view(request, pk):
    event = get_object_or_404(Event, pk=pk, organiser=request.user)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
        return redirect('organiser_dashboard')

    return render(request, 'events/event_confirm_delete.html', {'event': event})


@login_required
def event_update_post_view(request, pk):
    event = get_object_or_404(Event, pk=pk, organiser=request.user)

    if request.method == 'POST':
        form = EventUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.event = event
            update.save()
            messages.success(request, 'Update posted.')
            return redirect('event_detail', pk=pk)
    else:
        form = EventUpdateForm()

    return render(request, 'events/event_update_form.html', {'form': form, 'event': event})


@login_required
def organiser_dashboard_view(request):
    if request.user.role != 'organiser':
        return redirect('event_list')

    events = Event.objects.filter(organiser=request.user).order_by('-created_at')
    return render(request, 'events/organiser_dashboard.html', {'events': events})
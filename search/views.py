from django.shortcuts import render
from events.models import Event


def search_events(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')

    events = Event.objects.filter(status='approved')

    if query:
        events = events.filter(title__icontains=query)

    if category:
        events = events.filter(category__icontains=category)

    if location:
        events = events.filter(location__icontains=location)

    context = {
        'events': events,
        'query': query,
        'category': category,
        'location': location,
    }
    return render(request, 'search/search.html', context)


def matched_events(request):
    if not request.user.is_authenticated:
        return render(request, 'search/search.html', {'events': []})

    try:
        interests = request.user.profile.interests
        location = request.user.profile.location
    except:
        interests = ''
        location = ''

    events = Event.objects.filter(status='approved')

    if interests:
        interest_list = [i.strip() for i in interests.split(',')]
        from django.db.models import Q
        query = Q()
        for interest in interest_list:
            query |= Q(category__icontains=interest) | Q(title__icontains=interest)
        events = events.filter(query)

    if location:
        events = events.filter(location__icontains=location)

    return render(request, 'search/matched.html', {'events': events})
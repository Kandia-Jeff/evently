from django.db import models
from events.models import Event


class EventView(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'View on {self.event.title} at {self.viewed_at}'
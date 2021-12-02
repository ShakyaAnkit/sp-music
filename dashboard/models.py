from django.apps import apps
from django.db import models
from django.utils import timezone


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save()
        else:
            super().delete()


class Designation(DateTimeModel):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=(
        ('FEMALE', 'FEMALE'),
        ('MALE', 'MALE'),
        ('OTHERS', 'OTHERS'),
    ))
    date_of_birth = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations' 

    def __str__(self):
        return self.name

class CurrentPlayBack:
    def __str__(self):
        return self.device_id
    
    @classmethod
    def from_playback(cls, playback):
        current_playback = cls()
        current_playback.name = playback['item']['name']
        current_playback.artist = playback['item']['artists'][0]['name']
        current_playback.device_id = playback['device']['id']
        current_playback.image_url = playback['item']['album']['images'][0]['url']
        current_playback.track_uri = playback['item']['uri']
        current_playback.context_uri = playback['context']['uri']
        current_playback.duration = playback['item']['duration_ms']
        current_playback.preview_url = playback['item']['preview_url']
        current_playback.progress = playback['progress_ms']
        current_playback.is_playing = playback['is_playing']
        
        return current_playback


class FeaturedTrack:
    def __str__(self):
        return self.name

    @classmethod
    def from_track(cls, playback):
        track = cls()
        track.name = playback['name']
        track.artist = playback['artists'][0]['name']
        track.image_url = playback['images'][0]['url']
        track.track_uri = playback['uri']
        
        return track

class PlayListTrack:
    def __str__(self):
        return self.name

    @classmethod
    def from_track(cls, playback, context_uri):
        track = cls()
        track.name = playback['track']['name']
        track.artist = playback['track']['album']['artists'][0]['name']
        track.image_url = playback['track']['album']['images'][0]['url']
        track.duration = playback['track']['duration_ms']
        track.track_uri = playback['track']['uri']
        track.context_uri = context_uri
        
        return track
        
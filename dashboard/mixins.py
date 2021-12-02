import spotipy
from spotipy.oauth2 import SpotifyOAuth

from django.conf import settings as conf_settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .utils import get_current_playback, get_device, get_sp, get_featured_tracks

User = get_user_model()

class NonDeletedListMixin:
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class GetDeleteMixin:
    def get(self, request, *args, **kwargs):
        if hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class SuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class NonSuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class NonLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('dashboard:login')

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_superuser or self.request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class BaseMixin():
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_track'] = get_current_playback()
        context['featured_tracks'] = get_featured_tracks()
        print(get_device())
        return context

class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class GroupRequiredMixin(object):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or self.request.user.groups.filter(name__in=self.group_required).exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

# class SpotifyAuthentication:
#     def get_spotify_sp(self):
#         scope = "playlist-modify-public user-read-recently-played user-read-playback-state user-top-read app-remote-control user-modify-playback-state user-read-currently-playing user-read-playback-position playlist-read-collaborative streaming"
            
#         sp_auth=SpotifyOAuth(scope=scope, client_id=conf_settings.SPOTIFY_CLIENT_ID, client_secret=conf_settings.SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:8000/dashboard/')

#         url = sp_auth.get_authorize_url()

#         # sp = spotipy.Spotify(auth_manager=sp_auth)

#         auth_token=sp_auth.get_cached_token()

#         sp = spotipy.Spotify(auth=auth_token['access_token'])

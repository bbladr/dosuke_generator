from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Event, Band
from .forms import EventForm
from .functions import getTimetable, getTimeLavel

# Create your views here.
# イベント一覧画面
class EventListView(LoginRequiredMixin, ListView):
    model = Event

# イベント詳細画面
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bands'] = Band.objects.filter(event__name=context['event']).all()
        return context


# イベント作成画面
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = "/"

# イベント更新画面
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_url = "/"

# イベント削除画面
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = "/"


# 生成結果画面
class EventGenerateView(TemplateView):
    model = Event
    template_name = "dosuke/result.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timetables'] = getTimetable()
        context['labels'] = getTimeLavel()
        return context
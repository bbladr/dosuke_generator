from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Item, Event
from .forms import ItemForm
from .functions import getTimetable, getTimeLavel

# Create your views here.
# 検索一覧画面
class EventView(LoginRequiredMixin, FilterView):
    model = Event
    
    def get(self, request, **kwargs):
        print('print!')
        return super().get(request, **kwargs)

# 詳細画面
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event

    def get(self, request, **kwargs):
        print('Event!')
        return super().get(request, **kwargs)

# 登録画面
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 削除画面
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')


# 生成結果画面
class EventGenerateView(TemplateView):
    model = Event
    template_name = "dosuke/result.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timetables'] = getTimetable()
        context['labels'] = getTimeLavel()
        return context
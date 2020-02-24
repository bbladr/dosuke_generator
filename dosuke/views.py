from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from .models import Band, Member
from .forms import BandForm, MemberForm
from .functions import getTimetable, getTimeLavel

# 生成結果画面
class EventGenerateView(TemplateView):
    template_name = "dosuke/result.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timetables'] = getTimetable()
        context['time_labels'] = getTimeLavel()
        return context


### バンド
# バンド一覧画面
class BandListView(LoginRequiredMixin, ListView):
    model = Band

# バンド詳細画面
class BandDetailView(LoginRequiredMixin, DetailView):
    model = Band
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.filter(band__name=context['band']).all()
        return context


# バンド作成画面
class BandCreateView(LoginRequiredMixin, CreateView):
    model = Band
    form_class = BandForm
    success_url = "/band/"

# バンド更新画面
class BandUpdateView(LoginRequiredMixin, UpdateView):
    model = Band
    form_class = BandForm
    success_url = "/band/"
    
    def post(self, request):
        form = self.form_class(request.POST)
        obj = form.save(commit=False)
        obj.save()
        return redirect('event_detail', pk=obj.pk)

# バンド削除画面
class BandDeleteView(LoginRequiredMixin, DeleteView):
    model = Band
    success_url = "/band/"


### メンバー
# メンバー一覧画面
class MemberListView(LoginRequiredMixin, ListView):
    model = Member

# メンバー詳細画面
class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bands'] = Band.objects.filter(event__name=context['event']).all()
    #     return context

# メンバー作成画面
class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    success_url = "/member/"

# メンバー更新画面
class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    success_url = "/member/"

# メンバー削除画面
class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    success_url = "/member/"


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "dosuke/schedule.html"
    success_url = "/result"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bands'] = Band.objects.all()
        context['time_labels'] = getTimeLavel()
        return context

    def post(self, request):
        print(request.POST)
        # obj = form.save(commit=False)
        # obj.save()
        return redirect('/')
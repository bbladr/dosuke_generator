from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse

from .models import Band, Member
from .forms import BandForm, MemberForm
from .functions import getTimetables, getTimeLavel

import re

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

    def post(self, request):
        form = self.form_class(request.POST)
        obj = form.save(commit=False)
        obj.save()
        # ManyToMany の場合これを追記しないと save されない
        # see: https://qiita.com/tatamyiwathy/items/3ab83ab95c0ce62ede6e
        form.save_m2m()

        print(request.POST)
        return redirect('band_detail', pk=obj.pk)

# バンド更新画面
class BandUpdateView(LoginRequiredMixin, UpdateView):
    model = Band
    form_class = BandForm

    def get_success_url(self):
        return reverse('band_detail', kwargs={
            'pk': self.object.pk,
        })

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
    
    def get_context_data(self, **kwargs):
        # TODO 参加中のバンドを表示する
        return context

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

# スケジュール入力画面
class GenerateView(LoginRequiredMixin, TemplateView):
    template_name = "dosuke/generate.html"
    success_url = "/result"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bands'] = Band.objects.all()
        context['time_labels'] = getTimeLavel()
        return context

# 生成結果画面
class ResultView(TemplateView):
    template_name = "dosuke/result.html"
    
    # TODO パスに param が入るのが単純にダサいので Result モデルを作るか、generate ページの POST で1ページに収めるかする
    def get(self, request, **kwargs):
        # まずは req から必要な値を抽出
        params = {}
        for key in [key for key in request.GET if re.search('_', key)]: # アンダーバーが入っていたら希望時間用の値として判断する
            params[key] = int(request.GET[key])
        context = {
            'timetables': [['a']],
            'time_labels': getTimeLavel()
        }
        return self.render_to_response(context)
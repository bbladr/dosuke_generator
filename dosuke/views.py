from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import Band, Member, Config
from .forms import BandForm, MemberForm, ConfigForm
from .functions import get_timetables, get_time_label, get_timetables_with_pulp, get_timetables_abnormal

import pandas as pd

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
        context['time_labels'] = get_time_label()
        session_start = int(Config.objects.get(key='session_start').value)
        session_end = int(Config.objects.get(key='session_end').value)
        context['session_frames'] = range(session_start, session_end)
        room_start = int(Config.objects.get(key='room_start').value)
        room_end = int(Config.objects.get(key='room_end').value)    
        context['room_frames'] = range(room_start, room_end)
        max_days = int(Config.objects.get(key='max_days').value)
        context['days'] = range(1,max_days+1)
        return context

# 生成結果画面
class ResultView(TemplateView):
    template_name = "dosuke/result.html"
    
    def post(self, request, **kwargs):
        # まずは req から必要な値を抽出
        data_list = []

        # [TODO] クエリ数が多すぎて DATA_UPLOAD_MAX_NUMBER_FIELDS を変更(../Dosuke_pro/settings.py)して許容してるので data を使うようにする
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                continue
            elif key == 'method-radio':
                method = request.POST['method-radio']
                continue

            # アンダーバーを境目にバンド名とコマ番を取得
            band, day, time = key.split('_')
            data_list.append([band, int(day), int(time)])

        data = pd.DataFrame(data_list, columns=['band', 'day', 'hour'])

        if method == 'legacy':
            timetable_dict = get_timetables(data)
        elif method == 'pulp':
            timetable_dict = get_timetables_with_pulp(data)
        elif method == 'ab-pulp':
            timetable_dict = get_timetables_abnormal(data)
        else:
            timetable_dict = get_timetables(data)

        context = {
            'timetable_dict': timetable_dict,
            'time_labels': get_time_label()
        }
        return self.render_to_response(context)

# 設定画面
class SettingView(FormView):
    template_name = 'dosuke/setting.html'
    form_class = ConfigForm

    def post(self, request, **kwargs):
        form = ConfigForm(request.POST)
        if form.is_valid():
            for key in request.POST:
                if key == 'csrfmiddlewaretoken':
                    continue
                config = Config.objects.get(key=key)
                config.value = request.POST[key]
                config.save()
        messages.success(request, '更新しました。')
        return redirect('setting')
        # return request

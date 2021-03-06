from django.urls import path
from . import views

urlpatterns = [
    # バンド一覧画面
    path('band/',  views.BandListView.as_view(), name='band_list'),
    # バンド詳細画面
    path('band/detail/<int:pk>/', views.BandDetailView.as_view(), name='band_detail'),
    # バンド作成画面
    path('band/create/', views.BandCreateView.as_view(), name='band_create'),
    # バンド更新画面
    path('band/update/<int:pk>/', views.BandUpdateView.as_view(), name='band_update'),
    # バンド削除画面
    path('band/delete/<int:pk>/', views.BandDeleteView.as_view(), name='band_delete'),
    # メンバー一覧画面
    path('member/',  views.MemberListView.as_view(), name='member_list'),
    # メンバー詳細画面
    path('member/detail/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    # メンバー作成画面
    path('member/create/', views.MemberCreateView.as_view(), name='member_create'),
    # メンバー更新画面
    path('member/update/<int:pk>/', views.MemberUpdateView.as_view(), name='member_update'),
    # メンバー削除画面
    path('member/delete/<int:pk>/', views.MemberDeleteView.as_view(), name='member_delete'),
    # スケジュール入力画面
    path('', views.GenerateView.as_view(), name='generate'),
    # 土スケ生成結果画面
    path('result/', views.ResultView.as_view(), name='result'),
    # 設定画面
    path('setting/', views.SettingView.as_view(), name='setting'),
]
from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, EventGenerateView

urlpatterns = [
    # イベント一覧画面
    path('',  EventListView.as_view(), name='event_list'),
    # イベント詳細画面
    path('detail/<int:pk>/', EventDetailView.as_view(), name='detail'),
    # イベント作成画面
    path('create/', EventCreateView.as_view(), name='create'),
    # イベント更新画面
    path('update/<int:pk>/', EventUpdateView.as_view(), name='update'),
    # イベント削除画面
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='delete'),
    # 生成結果画面
    path('generate/<int:pk>/', EventGenerateView.as_view(), name='generate'),
    # バンド一覧画面
    path('band/',  EventListView.as_view(), name='band_index'),
    # バンド詳細画面
    path('band/detail/<int:pk>/', EventDetailView.as_view(), name='detail'),
    # バンド作成画面
    path('band/create/', EventCreateView.as_view(), name='create'),
    # バンド更新画面
    path('band/update/<int:pk>/', EventUpdateView.as_view(), name='update'),
    # バンド削除画面
    path('band/delete/<int:pk>/', EventDeleteView.as_view(), name='delete'),
]
from django.urls import path
from .views import EventView, EventDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, EventGenerateView

urlpatterns = [
    # 一覧画面
    path('',  EventView.as_view(), name='index'),
    # 生成結果画面
    path('generate/<int:pk>/', EventGenerateView.as_view(), name='generate'),
    # 詳細画面
    path('detail/<int:pk>/', EventDetailView.as_view(), name='detail'),
    # 登録画面
    path('create/', ItemCreateView.as_view(), name='create'),
    # 更新画面
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    # 削除画面
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
]
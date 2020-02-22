from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView
from .views import EventView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, EventViewSet

router = DefaultRouter()
router.register(r'Events', EventViewSet)

urlpatterns = [
    # 一覧画面
    path('',  EventView.as_view(), name='index'),
    # 詳細画面
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    # 登録画面
    path('create/', ItemCreateView.as_view(), name='create'),
    # 更新画面
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    # 削除画面
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    # api
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('redirect/', RedirectView.as_view(url='/static/html/index.html')),
]
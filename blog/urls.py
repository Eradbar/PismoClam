from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    selectBeach,
    PostDeleteView,
    DataDownload
)
from . import views
from blog.views import SurveyView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='survey-detail'),
    path('post/new/', SurveyView.as_view(), name='survey-create'),
    path('post/selectBeach/', selectBeach.as_view(), name='beach'),
    path('post/<int:pk>/update', SurveyView.as_view(), name='survey-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='survey-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/download/', DataDownload, name='blog-download_survey'),
]


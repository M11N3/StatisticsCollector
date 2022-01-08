from django.urls import path

from .views import StatisticAPIView

urlpatterns = [
    path('statistic/', StatisticAPIView.as_view()),
]

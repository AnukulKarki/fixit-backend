
from django.urls import path
from .views import BadgeView,BadgeViewData



urlpatterns = [
    path('view/', BadgeView.as_view()),
    path('view/<int:id>', BadgeViewData.as_view()),
]
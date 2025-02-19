from django.urls import path
from .views import GigPostView, GigListView, GigDeleteView, GigEditView, GigDetailView, GigListAllView,GigSearch
# Url = api/worker/gig/
urlpatterns = [
    path('post/', GigPostView.as_view()),
    path('list/', GigListView.as_view()),
    path('list-all/', GigListAllView.as_view()),
    
    path('delete/<int:id>/', GigDeleteView.as_view()),
    path('edit/<int:id>/', GigEditView.as_view()),
    path('detail/<int:id>/', GigDetailView.as_view()),
    path('search/<str:search>/', GigSearch.as_view()),
]
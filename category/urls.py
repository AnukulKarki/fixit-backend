from django.urls import path
from .views import CategoryListView, CategoryAddView, CategoryAdd, CategoryDeleteView, CategoryEditView,CategoryEditView
#api/category
urlpatterns = [
    path('list/',  CategoryListView.as_view() ),
    path('add/',  CategoryAddView.as_view() ),
    path('add/data/',  CategoryAdd.as_view() ),
    path('delete/<int:id>/',  CategoryDeleteView.as_view() ),
    path('edit/<int:id>/',  CategoryEditView.as_view() ),
]
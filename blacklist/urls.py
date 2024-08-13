from django.urls import path
from .views import  BlacklistAddView,BlacklistRemoveView, BlacklistListView
#api/admin/blacklist/
urlpatterns = [
    path('add/<int:id>/',  BlacklistAddView.as_view() ),
    path('remove/<int:id>/',  BlacklistRemoveView.as_view() ),
    path('list/',  BlacklistListView.as_view() ),
]
from django.urls import path
from .views import BrandItemPostView, BrandPostView, BrandList, BrandItemList, BrandItemListDetail,BrandItemDelete,BrandEdit,BrandDelete
#api/admin/brand/
urlpatterns = [
    path('post/',  BrandPostView.as_view() ),
    path('item/post/',  BrandItemPostView.as_view() ),
    path('list/',  BrandList.as_view()),
    path('item/list/',  BrandItemList.as_view()),
    path('brand-item/list/<int:id>/',  BrandItemListDetail.as_view()),
    path('brand-item/delete/<int:id>/',  BrandItemDelete.as_view()),
    path('edit/<int:id>/',  BrandEdit.as_view()),
    path('delete/<int:id>/',  BrandDelete.as_view()),
    
]
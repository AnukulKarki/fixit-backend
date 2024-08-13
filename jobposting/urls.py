from django.urls import path
from .views import JobRequirementPostView, NearJobRequirementListView, ProposalNumber,JobFilter, JobRequirementEditView, JobRequirementDeleteView, JobRequirementDetailView, JobRequirementListView, JobRequirementListViewUser, JobRequirementUserDetailView
#api/job/
urlpatterns = [
    path('post/',  JobRequirementPostView.as_view() ), #Post
    path('edit/<int:id>/', JobRequirementEditView.as_view() ), #edit the job requirement
    path('delete/<int:id>/', JobRequirementDeleteView.as_view() ), # delete the job requriement by the users
    path('detail/<int:id>/', JobRequirementDetailView.as_view() ), # can watch the details of every job requirements   -> Used to display details
    path('user/detail/<int:id>/', JobRequirementUserDetailView.as_view() ), #can only watch the detais of the job requirement of logged in user --> 
    path('list-all/', JobRequirementListView.as_view() ), # list all the job req
    path('user/list/', JobRequirementListViewUser.as_view() ), #list the job req that is posted by the user only
    path('filter/<int:category>/<int:minprice>/<int:maxprice>/', JobFilter.as_view() ), #list the job req that is posted by the user only
    path('count/<int:id>/', ProposalNumber.as_view() ), #list the job req that is posted by the user only
    path('distance', NearJobRequirementListView.as_view()) 
]
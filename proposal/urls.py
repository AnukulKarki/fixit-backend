from django.urls import path
from .views import ProposalAppliedWorkerView, ProposalApplyView, PendingProposalWorkerView, PastProposalWorkerView,ProposalDeleteView
from workerhire.views import WorkerHire, WorkerRejectView
#api/worker/proposal/
urlpatterns = [
    path('apply/<int:id>/',  ProposalApplyView.as_view() ), #proposal Apply  -> id = jobreq id
    path('list/<int:id>/',  ProposalAppliedWorkerView.as_view() ), #proposal Listing -> -> id = jobreq id
    path('hire/<int:id>/<int:jobid>/',  WorkerHire.as_view() ), #id = proposal id, jobid = job oid
    path('reject/<int:id>/',  WorkerRejectView.as_view() ), #id = proposal id, jobid = job oid
    path('pending/',  PendingProposalWorkerView.as_view() ), #id = proposal id, jobid = job oid
    path('past/',  PastProposalWorkerView.as_view() ), #id = proposal id, jobid = job oid
    path('delete/<int:id>/',  ProposalDeleteView.as_view() ), #id = proposal id, jobid = job oid
]
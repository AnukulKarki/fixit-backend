from django.urls import path
from .views import GigProposalApplyView, GigProposalListview, GigProposalAcceptView, GigProposalRejectView, CurrentGigWorkView, CurrentGigWorkClientView, GigWorkStartView, GigWorkCompleteView, GigWorkCancelView, GigWorkPayView, RatingView, GigProposalDetailview, GigProposalClientRequest, deleteProposal, GigWorkDetail, GigPastWork, GigPastWorkClient
from .views import GigPastWorkId, GigPastWorkClientId,ReportList, ReportWork
#api/hire/
urlpatterns = [
    path('proposal/<int:id>/', GigProposalApplyView.as_view()), #id -> worker
    path('list/', GigProposalListview.as_view()),
    path('detail/<int:id>/', GigProposalDetailview.as_view()),
    path('proposal/accept/<int:id>/', GigProposalAcceptView.as_view()),#id = proposal id
    path('proposal/reject/<int:id>/', GigProposalRejectView.as_view()),#id = proposal id
    path('current-work/', CurrentGigWorkView.as_view()),
    path('current-work/client/', CurrentGigWorkClientView.as_view()),

    path('work/progress/<int:id>/', GigWorkStartView.as_view()),

    path('work/complete/<int:id>/', GigWorkCompleteView.as_view()),

    path('work/cancel/<int:id>/', GigWorkCancelView.as_view()),

    path('work/pay/<int:id>/', GigWorkPayView.as_view()),
    path('work/rating/<int:id>/', RatingView.as_view()),
    path('client/proposal/list/', GigProposalClientRequest.as_view()),
    path('client/proposal/delete/<int:id>/', deleteProposal.as_view()),
    path('work/detail/<int:id>/', GigWorkDetail.as_view()),

    path('past-work/', GigPastWork.as_view()),
    path('past-work/<int:id>/', GigPastWorkId.as_view()),
    path('past-work/client/', GigPastWorkClient.as_view()),
    path('past-work/client/<int:id>/', GigPastWorkClientId.as_view()),
    path('reportdata/<int:id>/', ReportList.as_view()),
    path('report/<int:id>/', ReportWork.as_view()),
    
]
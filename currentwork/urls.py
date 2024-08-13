from django.urls import path
from .views import CurrentWorkerWorkView, startProgress, CancelCurrentWorkerView, PayWorkView, CurrentWorkerClientView, RatingView, PastWorkViewWorker, PastWorkViewClient, WorkDescriptionView, verifyKhalti
from .views import KhaltiPayment, PastWorkViewWorkerId,PastWorkViewClientId, ReportWork
#api/work
urlpatterns = [
    path('current-work/', CurrentWorkerWorkView.as_view()),
    path('client/current-work/', CurrentWorkerClientView.as_view()),
    path('worker/cancel-work/<int:id>/', CancelCurrentWorkerView.as_view()),
    path('progress/<int:id>/', startProgress.as_view()),
    path('pay-work/<int:id>/', PayWorkView.as_view()),
    path('rate/<int:id>/', RatingView.as_view()),
    path('past-work/', PastWorkViewWorker.as_view()),
    path('past-work/<int:id>/', PastWorkViewWorkerId.as_view()),
    path('client/past-work/', PastWorkViewClient.as_view()),
    path('client/past-work/<int:id>/', PastWorkViewClientId.as_view()),
    path('work/<int:id>/', WorkDescriptionView.as_view()),
    path('khalti',KhaltiPayment.as_view()),
    path('khalti-verify/<int:id>/<int:key>/',verifyKhalti.as_view()),
    path('report/<int:id>/',ReportWork.as_view())
]
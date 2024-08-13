from django.urls import path
from .views import RegistrationUser,passwordHash,PersonalWorkerDetailProfile,AdminUserUpdate,verifyUser, ChangePassword,PasswordChange,profileEdit, loginUser, profileView, LogoutView, UserCheck, userProfileId, workerList, ClientList, CodeVerification, ResendCode, ClientDetailProfile, WorkerDetailProfile
from .emails import sendEmail

urlpatterns = [
    path('register/', RegistrationUser.as_view() ),
    path('login/', loginUser.as_view()),
    path('profile/', profileView.as_view()),
    path('profile/edit/', profileEdit.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user-check/', UserCheck.as_view()),
    path('change-password/', PasswordChange.as_view()),
    path('user-profile/<int:id>/', userProfileId.as_view()),
    path('client-list/', ClientList.as_view()),
    path('worker-list/', workerList.as_view()),
    path('email/', sendEmail.as_view()),
    path('code/verify/', CodeVerification.as_view()),
    path('code/resend/', ResendCode.as_view()),
    path('client-detail/<int:id>/', ClientDetailProfile.as_view()),
    path('worker-detail/<int:id>/', WorkerDetailProfile.as_view()),
    path('user-verify/<int:id>/', verifyUser.as_view()),
    path('forgetpassword/', ChangePassword.as_view()),
    path('edit/<int:id>/', AdminUserUpdate.as_view()),
    path('worker-data/', PersonalWorkerDetailProfile.as_view()),
]
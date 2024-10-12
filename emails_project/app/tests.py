from django.urls import path
from .views import RegistrationView, VerificationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('verify/<uuid:token>/', VerificationView.as_view(), name='verify'),
]

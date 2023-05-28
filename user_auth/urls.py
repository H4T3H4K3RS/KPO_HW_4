from django.urls import path
from .views import RegistrationView, LoginView, GetUserView

urlpatterns = [
    path('api/user/register/', RegistrationView.as_view()),
    path('api/user/login/', LoginView.as_view()),
    path('api/user/me/', GetUserView.as_view()),
]

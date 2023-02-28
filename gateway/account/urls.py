from django.urls import path

from account.views import UserView, AccountView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('account/', AccountView.as_view()),
]

from django.urls import path

from account.views import UserView, AccountView, GoogleAuthView, UserPlayerToken

urlpatterns = [
    path('user/', UserView.as_view()),
    path('account/', AccountView.as_view()),
    path('google/', GoogleAuthView.as_view()),
    path('user_player/', UserPlayerToken.as_view()),
]

from django.urls import path

from notification.views import NotificationView

urlpatterns = [
    path('notifications/', NotificationView.as_view()),
]

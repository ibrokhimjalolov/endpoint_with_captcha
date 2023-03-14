from django.urls import path

from .views import ProtectedView, NotProtectedView

urlpatterns = [
    path("protected-view", ProtectedView.as_view(), name="protected-view"),
    path("not-protected-view", NotProtectedView.as_view(), name="not-protected-view"),
]

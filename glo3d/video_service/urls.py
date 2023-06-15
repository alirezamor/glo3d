from django.urls import path
from .views import FrameExtractionView


urlpatterns = [
    path('extract-frames/', FrameExtractionView.as_view()),
]

from django.urls import path
from .views import RotateArrayView, KthLargestView, LongestIncreasingPathView

urlpatterns = [
    path("leetcode/rotate-array", RotateArrayView.as_view(), name="rotate-array"),
    path("leetcode/kth-largest/", KthLargestView.as_view(), name="kth-largest"),
    path("leetcode/longest-increasing-path/", LongestIncreasingPathView.as_view(), name="longest-increasing-path"),
]

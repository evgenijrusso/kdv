from django.urls import path
from callboard.views.index import Index
from callboard.views.confirm import ConfirmUser, UserProfileView

urlpatterns = [
    path('', Index.as_view(), name='index'),  # http://127.0.0.1:8027

    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('account/', Index.as_view(), name='index'),
]

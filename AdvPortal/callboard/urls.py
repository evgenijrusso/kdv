from django.urls import path
from callboard.views.index import Index
from callboard.views.confirm import ConfirmUser, UserProfileView
from callboard.views.advert import AdvertList, AdvertCreate, \
    AdvertDetail, AdvertUpdate, AdvertDelete
from callboard.views.response import ResponseList, ResponseDetail, \
    ResponseCreate, ResponseUpdate, ResponseDelete, PrivateView, accept_response, ReplyDelete


urlpatterns = [
    path('', Index.as_view(), name='index'),  # http://127.0.0.1:8027
    path('callboard/', AdvertList.as_view(), name='advert_list'),  # {% url "advert_list" %}
    path('callboard/<int:pk>', AdvertDetail.as_view(), name='advert_detail'),
    path('callboard/create', AdvertCreate.as_view(), name='advert_create'),
    path('callboard/update/<int:pk>', AdvertUpdate.as_view(), name='advert_update'),
    path('callboard/delete/<int:pk>', AdvertDelete.as_view(), name='advert_delete'),

    path('callboard/responses/', ResponseList.as_view(), name='response_list'),
    path('callboard/response/<int:pk>', ResponseDetail.as_view(), name='response_detail'),
    path('callboard/responses/create/', ResponseCreate.as_view(), name='response_create'),
    path('callboard/responses/update/<int:pk>', ResponseUpdate.as_view(), name='response_update'),
    path('callboard/responses/delete/<int:pk>', ResponseDelete.as_view(), name='response_delete'),

    path('callboard/responses/private', PrivateView.as_view(), name='private_response'),
    path('callboard/responses/<int:pk>', accept_response, name='accept_response'),
    path('callboard/responses/delete/<int:pk>',  ReplyDelete.as_view(), name='delete_response'),

    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('account/', Index.as_view(), name='index')
]

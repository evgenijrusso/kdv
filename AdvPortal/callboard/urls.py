from django.urls import path
from callboard.views.index import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),  # http://127.0.0.1:8027
]

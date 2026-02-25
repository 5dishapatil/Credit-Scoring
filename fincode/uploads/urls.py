from django.urls import path
from .views import upload_financials

urlpatterns = [
    path('', upload_financials, name='upload'),
]

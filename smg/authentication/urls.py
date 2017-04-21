from django.conf.urls import url
from .views import SignInView, AccountsViewSet


urlpatterns = [
    url(r'^sign-in/$', SignInView.as_view(), name='sign_in'),
    url(r'^accounts/$', AccountsViewSet.as_view({'get': 'list'}), name='accounts')
]

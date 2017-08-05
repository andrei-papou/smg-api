from django.conf.urls import url
from .views import SignInView, AccountsViewSet


urlpatterns = [
    url(r'^sign-in/$', SignInView.as_view(), name='sign_in'),
    url(r'^accounts/$', AccountsViewSet.as_view({'get': 'list'}), name='accounts'),
    url(r'^accounts/(?P<pk>[0-9]+)/$',
        AccountsViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name='accounts-detail'),
]

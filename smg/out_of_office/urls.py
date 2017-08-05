from django.conf.urls import url
from .views import TimeShiftView, BusinessLeaveView, UnpaidView, VacationView, IllnessView, ApproveView

urlpatterns = [
    url(r'^time-shifts/$', TimeShiftView.as_view(), name='time-shifts'),
    url(r'^business-leaves/$', BusinessLeaveView.as_view(), name='business-leaves'),
    url(r'^unpaids/$', UnpaidView.as_view(), name='unpaids'),
    url(r'^vacations/$', VacationView.as_view(), name='vacations'),
    url(r'^illnesses/$', IllnessView.as_view(), name='illnesses'),

    url(r'^all/(?P<pk>[0-9]+)/approve/$', ApproveView.as_view(), name='approve'),
]

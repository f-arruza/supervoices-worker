from django.conf.urls import url
from .views import (
    LogoutView,
    UserView,
    UpdateUserView,
    ChangePasswordView,
    login_user,
    verify_token,
)

urlpatterns = [
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', UserView.as_view(), name='users'),
    url(r'^update/(?P<pk>\d+)/$', UpdateUserView.as_view(),
        name='update_user'),
    url(r'^change_passwd/$', ChangePasswordView.as_view(),
        name='change_passwd'),
    url(r'^verify_token/$', verify_token, name='verify_token'),
]

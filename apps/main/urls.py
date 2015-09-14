from django.conf.urls import include, patterns, url

from .views import IndexView, WebMasterView, UserListView, ProfileListCreateView, ProfileRetrieveView, UserCreateView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^user$', UserListView.as_view(), name='user_list_view'),
    url(r'^create$', UserCreateView.as_view(), name='user_create_view'),
    url(r'^profile$', ProfileListCreateView.as_view(), name='profile_list_create_view'),
    url(r'^profile/(?P<pk>[0-9]+)$', ProfileRetrieveView.as_view(), name='user_list_view'),
)

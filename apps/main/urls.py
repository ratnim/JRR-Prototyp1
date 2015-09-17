from django.conf.urls import include, patterns, url

from .views import IndexView, ProfileCreateView, ProfileListView, ProfileRetrieveView, SuperuserCreateView,\
    ExpertListView, ExpertCreateView, ExpertLoginView, ExpertLogoutView, ExpertActivateView, \
    ExpertRetrieveView

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^api/v1/expert$', ExpertListView.as_view(), name='expert_list_view'),
    url(r'^api/v1/expert/create$', ExpertCreateView.as_view(), name='expert_create_view'),
    url(r'^api/v1/expert/login$', ExpertLoginView.as_view(), name='expert_login_view'),
    url(r'^api/v1/expert/logout$', ExpertLogoutView.as_view(), name='expert_logout_view'),
    url(r'^api/v1/expert/activate/(?P<pk>[0-9]+)$', ExpertActivateView.as_view(), name='expert_activate_view'),
    url(r'^api/v1/expert/(?P<pk>[0-9]+)$', ExpertRetrieveView.as_view(), name='expert_retrieve_view'),
    url(r'^api/v1/admin/create$', SuperuserCreateView.as_view(), name='superuser_create_view'),
    url(r'^api/v1/profile$', ProfileListView.as_view(), name='profile_list_view'),
    url(r'^api/v1/profile/create$', ProfileCreateView.as_view(), name='profile_create_view'),
    url(r'^api/v1/profile/(?P<pk>[0-9]+)$', ProfileRetrieveView.as_view(), name='profile_retrieve_view'),
)



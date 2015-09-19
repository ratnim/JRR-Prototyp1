from django.conf.urls import include, patterns, url

from .views import IndexView, ProfileCreateView, ProfileListView, ProfileRetrieveView,\
    ExpertListView, ExpertCreateView, ExpertLoginView, ExpertLogoutView, ExpertActivateView, \
    ExpertRetrieveView, ExpertOwnView
urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^api/v1/experts$', ExpertListView.as_view(), name='expert_list_view'),
    url(r'^api/v1/experts/create$', ExpertCreateView.as_view(), name='expert_create_view'),
    url(r'^api/v1/experts/login$', ExpertLoginView.as_view(), name='expert_login_view'),
    url(r'^api/v1/experts/logout$', ExpertLogoutView.as_view(), name='expert_logout_view'),
    url(r'^api/v1/experts/activate/(?P<pk>[0-9]+)$', ExpertActivateView.as_view(), name='expert_activate_view'),
    url(r'^api/v1/experts/(?P<pk>[0-9]+)$', ExpertRetrieveView.as_view(), name='expert_retrieve_view'),
    url(r'^api/v1/experts/own$', ExpertOwnView.as_view(), name='expert_own_view'),
    url(r'^api/v1/profiles$', ProfileListView.as_view(), name='profile_list_view'),
    url(r'^api/v1/profiles/create$', ProfileCreateView.as_view(), name='profile_create_view'),
    url(r'^api/v1/profiles/(?P<pk>[0-9]+)$', ProfileRetrieveView.as_view(), name='profile_retrieve_view'),

)




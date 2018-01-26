from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'portal'

urlpatterns = [
    url(r'^login_page/$',views.login_page,name='login_page'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^profile1/$', views.profile1_view, name='profile1'),
    url(r'^profile2/$', views.profile2_view, name='profile2'),
    url(r'^profile3/$', views.profile3_view, name='profile3'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^create_team_page/$', views.create_team_page, name='create_team_page'),
    url(r'^create_team/$',views.create_team,name='create_team'),
    url(r'^event_page/(?P<team_id>\d+)/$',views.apply_event_page,name='apply_event_page'),
    url(r'^search_event_page/$',views.search_event_page,name='search_event_page'),
    url(r'^apply_event/(?P<team_id>\d+)/$',views.apply_event,name='event'),
    url(r'^post/$',views.show_request_user2,name='show_request_user2'),
    url(r'^approve/$',views.approval_request_user,name='approve_request'),
    url(r'^approve_team/$',views.approval_team_request,name='approve_team_request'),
    url(r'^pending/$',views.show_pending_request,name='pending'),
    url(r'search_team/$',views.search_team),
    url(r'test/$',views.test ),
]
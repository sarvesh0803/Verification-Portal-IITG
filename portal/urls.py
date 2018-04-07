from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .views import GeneratePDF

app_name = 'portal'

urlpatterns = [
    url(r'^login_page/$',views.login_page,name='login_page'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^create_team_page/$', views.create_team_page, name='create_team_page'),
    url(r'^create_team/$',views.create_team,name='create_team'),
    # url(r'^event_page/(?P<team_id>\d+)/$',views.apply_event_page,name='apply_event_page'),
    url(r'^search_event_page/$',views.search_event_page,name='search_event_page'),
    url(r'^apply_event/(?P<team_id>\d+)/$',views.apply_event,name='event'),
    url(r'^approve/$',views.approval_request_user,name='approve_request'),
    url(r'^approve_team/$',views.approval_team_request,name='approve_team_request'),
    url(r'^pending/$',views.show_pending_request,name='pending'),
    url(r'search_team/$',views.search_team),
    # url(r'validate_post/$', views.validate_post),
    url(r'help/$',views.help,name = 'help' ),
    url(r'profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<roll_no>\w+)/(?P<id>\w+)/$',views.view_profile,name='view_profile'),
    url(r'profile_edit/$', views.edit_profile, name='profile_edit'),
    url(r'edit_profile_page/$', views.edit_profile_page, name='edit_profile_page'),
    url(r'error/$',views.error,name='error'),
    url(r'test/$',views.test,name='test'),
    url(r'^pdf/$',GeneratePDF.as_view(), name="pdf_generate"),
    url(r'feedback/$',views.feedback,name="feedback")
   ]

handler404 = 'portal.views.custom_404'
handler500 = 'portal.views.custom_500'


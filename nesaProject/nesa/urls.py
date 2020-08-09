from django.urls import path, re_path
from . import views
from jet.dashboard.dashboard_modules import google_analytics_views
from django.contrib.auth.decorators import login_required
from nesa.views import IndexView, LogoutView

# from django.utils.translation import ugettext_lazy as _
# from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
# from jet.dashboard.dashboard_modules import google_analytics


urlpatterns = [
    path('', views.index, name='index'),
    path('logindex', views.logindex, name='logindex'),
    path('contactus/', views.contactUs, name='contactUs'),
    path('rewards-blog-archive/', views.rewardsBlogArchive, name='rewards-blog-archive'),
    # path('rewards/<str:server>-<int:year>-<int:month>/', views.rewardsBlogSingle, name='rewards-blog-single'),
    path('rewards/<str:server>', views.rewardsBlogSingle_by_server, name='rewards-blog-single'),
    # path('rewards/<str:server>/<int:year>/<int:month>/', views.rewardsBlogSingle, name='rewards-blog-single'),
    path('rewards/<str:slug>/', views.rewardsBlogSingle_by_slug, name='rewards-blog-single'),
    # path('rewards/', views.rewardsBlogSingle, name='rewards-blog-single'),
    path('rewards-blog-grid/', views.rewardsBlogGrid, name='rewards-blog-grid'),
    path('news-blog-archive/', views.newsBlogArchive, name='news-blog-archive'),
    path('news/<str:slug>/', views.newsBlogSingle, name='news-blog-single'),
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^logout', login_required(LogoutView.as_view(), login_url='/'), name='logout')
]

# AJAX requests pattern
urlpatterns = urlpatterns + [
    path('get-approvement/', views.get_approvement, name='get-approvement'),
    path('is-registered', views.check_user_if_registered, name='is-registered'),
    path('save-user-detail', views.save_user_detail, name='save-user-detail'),
    path('save-comment', views.save_comment, name='save-comment'),
    path('save-contact-us', views.save_contact_us, name='save-contact-us')
]

# class CustomIndexDashboard(Dashboard):
#     columns = 3

#     def init_with_context(self, context):
#        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
#        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
#        self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)

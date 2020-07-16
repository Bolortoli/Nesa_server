from django.urls import path
from . import views
from jet.dashboard.dashboard_modules import google_analytics_views
# from django.utils.translation import ugettext_lazy as _
# from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
# from jet.dashboard.dashboard_modules import google_analytics


urlpatterns = [
    path('', views.index, name='home'),
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
    path('news-blog-single/', views.newsBlogSingle, name='news-blog-single'),
]



# class CustomIndexDashboard(Dashboard):
#     columns = 3

#     def init_with_context(self, context):
#        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
#        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
#        self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)

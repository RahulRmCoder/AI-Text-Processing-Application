from django.urls import path
from . import views

urlpatterns = [
    # Web interface URLs
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history_view, name='history'),
    path('clear-history/', views.clear_history, name='clear_history'),
    
    # API endpoints
    path('api/summarize/', views.SummarizeView.as_view(), name='api_summarize'),
    path('api/rewrite/', views.RewriteView.as_view(), name='api_rewrite'),
    path('api/history/', views.UserHistoryView.as_view(), name='api_history'),
]
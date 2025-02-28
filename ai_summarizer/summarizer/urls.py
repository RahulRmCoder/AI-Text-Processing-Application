from django.urls import path
from .views import SummarizeView, RewriteView, frontend_view

urlpatterns = [
    # API endpoints
    path('api/summarize/', SummarizeView.as_view(), name='summarize'),
    path('api/rewrite/', RewriteView.as_view(), name='rewrite'),
    
    # Frontend view
    path('', frontend_view, name='frontend'),
]
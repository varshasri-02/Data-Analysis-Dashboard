from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('export/', views.export_csv, name='export_csv'),
    path('export/missing/', views.export_missing_report, name='export_missing'),
    path('export/correlation/', views.export_correlation_matrix, name='export_correlation'),
    # API endpoints
    path('api/analyze/', views.AnalyzeCSVAPIView.as_view(), name='api_analyze'),
    path('api/download/', views.DownloadCleanedCSVAPIView.as_view(), name='api_download'),
]

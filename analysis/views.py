import pandas as pd
import numpy as np
import os
import uuid
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
from .utils import perform_full_analysis
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CSVUploadSerializer
import io
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def handle_uploaded_file(file):
    # Clean old files (older than 1 hour)
    clean_old_files()

    # Generate unique filename
    ext = os.path.splitext(file.name)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(unique_filename, file)
    return fs.path(filename)

def clean_old_files():
    """Clean uploaded files older than 1 hour"""
    media_dir = settings.MEDIA_ROOT
    if not os.path.exists(media_dir):
        return

    now = datetime.now()
    for filename in os.listdir(media_dir):
        filepath = os.path.join(media_dir, filename)
        if os.path.isfile(filepath):
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if now - mtime > timedelta(hours=1):
                try:
                    os.remove(filepath)
                except OSError:
                    pass  # Ignore errors

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_path = handle_uploaded_file(request.FILES['file'])
                # Try different encodings
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(file_path, encoding='latin1')
                    except UnicodeDecodeError:
                        raise ValueError("Unable to decode CSV file. Please ensure it's a valid CSV with proper encoding.")

                # Check for missing headers
                if df.empty:
                    raise ValueError("CSV file is empty.")
                if df.columns.isnull().any():
                    raise ValueError("CSV file has missing column headers.")

                # Check for minimum data
                if len(df) == 0:
                    raise ValueError("CSV file contains no data rows.")

                # Perform full analysis
                analysis_results = perform_full_analysis(df)

                # Prepare data for template
                summary_stats = df.describe().to_html()
                head = df.head().to_html()
                missing_values = analysis_results['missing_analysis'].to_html()
                duplicates = analysis_results['duplicates']['total_duplicates']
                data_overview = analysis_results['overview']
                column_summaries = analysis_results['column_summaries']
                correlation_matrix = analysis_results['correlation_matrix'].to_html() if not analysis_results['correlation_matrix'].empty else None
                outliers = analysis_results['outliers']

                # Generate visualizations (base64 encoded)
                charts = []

                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

                # Histogram for each numeric column (up to 3)
                if len(numeric_cols) > 0:
                    for col in numeric_cols[:3]:
                        plt.figure(figsize=(8, 6))
                        df[col].hist(bins=20, edgecolor='black')
                        plt.title(f'Distribution of {col}')
                        plt.xlabel(col)
                        plt.ylabel('Frequency')
                        buffer = BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        plt.close()
                        charts.append({
                            'type': 'histogram',
                            'title': f'Histogram: {col}',
                            'data': f'data:image/png;base64,{image_base64}'
                        })

                # Box plot for each numeric column (up to 2)
                if len(numeric_cols) > 0:
                    for col in numeric_cols[:2]:
                        plt.figure(figsize=(8, 6))
                        df.boxplot(column=col)
                        plt.title(f'Box Plot: {col}')
                        buffer = BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        plt.close()
                        charts.append({
                            'type': 'boxplot',
                            'title': f'Box Plot: {col}',
                            'data': f'data:image/png;base64,{image_base64}'
                        })

                # Correlation heatmap
                if len(numeric_cols) > 1:
                    plt.figure(figsize=(10, 8))
                    correlation_matrix = df[numeric_cols].corr()
                    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
                    plt.title('Correlation Heatmap')
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    plt.close()
                    charts.append({
                        'type': 'heatmap',
                        'title': 'Correlation Heatmap',
                        'data': f'data:image/png;base64,{image_base64}'
                    })

                # Scatter matrix (pairplot) for first 4 numeric columns
                if len(numeric_cols) >= 2:
                    pair_cols = numeric_cols[:4] if len(numeric_cols) > 4 else numeric_cols
                    plt.figure(figsize=(12, 12))
                    pd.plotting.scatter_matrix(df[pair_cols], alpha=0.2, figsize=(12, 12), diagonal='hist')
                    plt.suptitle('Scatter Matrix')
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    plt.close()
                    charts.append({
                        'type': 'scatter_matrix',
                        'title': 'Scatter Matrix',
                        'data': f'data:image/png;base64,{image_base64}'
                    })

                # Bar chart for categorical columns (up to 2)
                if len(categorical_cols) > 0:
                    for col in categorical_cols[:2]:
                        plt.figure(figsize=(10, 6))
                        df[col].value_counts().plot(kind='bar')
                        plt.title(f'Distribution of {col}')
                        plt.xlabel(col)
                        plt.ylabel('Count')
                        plt.xticks(rotation=45)
                        buffer = BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        plt.close()
                        charts.append({
                            'type': 'bar_chart',
                            'title': f'Bar Chart: {col}',
                            'data': f'data:image/png;base64,{image_base64}'
                        })

                # Line plot if time-series detected
                date_cols = []
                for col in df.columns:
                    try:
                        pd.to_datetime(df[col])
                        date_cols.append(col)
                    except:
                        pass
                if date_cols:
                    time_col = date_cols[0]
                    df[time_col] = pd.to_datetime(df[time_col])
                    df = df.sort_values(time_col)
                    numeric_for_time = [col for col in numeric_cols if col != time_col][:2]
                    if numeric_for_time:
                        plt.figure(figsize=(12, 6))
                        for col in numeric_for_time:
                            plt.plot(df[time_col], df[col], label=col)
                        plt.title('Time Series Plot')
                        plt.xlabel(time_col)
                        plt.ylabel('Value')
                        plt.legend()
                        buffer = BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        plt.close()
                        charts.append({
                            'type': 'line_plot',
                            'title': 'Time Series Plot',
                            'data': f'data:image/png;base64,{image_base64}'
                        })

                # Store file path in session for export functionality
                request.session['uploaded_file_path'] = file_path

                context = {
                    'form': form,
                    'summary_stats': summary_stats,
                    'head': head,
                    'missing_values': missing_values,
                    'duplicates': duplicates,
                    'data_overview': data_overview,
                    'numeric_summary': column_summaries['numeric'].to_html() if not column_summaries['numeric'].empty else None,
                    'categorical_summary': column_summaries['categorical'].to_html() if not column_summaries['categorical'].empty else None,
                    'correlation_matrix': correlation_matrix,
                    'outliers': outliers,
                    'charts': charts,
                    'charts_generated': len(charts),
                }
                return render(request, 'analysis/result.html', context)
            except Exception as e:
                form.add_error(None, f"Error processing file: {str(e)}")
            except Exception as e:
                form.add_error(None, f"Error processing file: {str(e)}")
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})


def export_csv(request):
    """Export cleaned CSV data"""
    if request.method == 'POST':
        # Get the uploaded file from session
        file_path = request.session.get('uploaded_file_path')
        if file_path and os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Clean the data
            cleaned_df = perform_full_analysis(df)['cleaned_data']

            # Create response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="cleaned_data.csv"'

            # Write to response
            cleaned_df.to_csv(response, index=False)
            return response

    return HttpResponse("File not found or invalid request", status=400)


class AnalyzeCSVAPIView(APIView):
    """API endpoint for CSV analysis"""

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = serializer.create_analysis_result()
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DownloadCleanedCSVAPIView(APIView):
    """API endpoint for downloading cleaned CSV"""

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                file = serializer.validated_data['file']
                df = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8')
                cleaned_df = perform_full_analysis(df)['cleaned_data']

                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="cleaned_data.csv"'
                cleaned_df.to_csv(response, index=False)
                return response
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def export_missing_report(request):
    """Export missing values report"""
    if request.method == 'POST':
        file_path = request.session.get('uploaded_file_path')
        if file_path and os.path.exists(file_path):
            df = pd.read_csv(file_path)
            analysis_results = perform_full_analysis(df)
            missing_report = analysis_results['missing_analysis']

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="missing_values_report.csv"'
            missing_report.to_csv(response)
            return response

    return HttpResponse("File not found or invalid request", status=400)

def export_correlation_matrix(request):
    """Export correlation matrix"""
    if request.method == 'POST':
        file_path = request.session.get('uploaded_file_path')
        if file_path and os.path.exists(file_path):
            df = pd.read_csv(file_path)
            analysis_results = perform_full_analysis(df)
            corr_matrix = analysis_results['correlation_matrix']

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="correlation_matrix.csv"'
            corr_matrix.to_csv(response)
            return response

    return HttpResponse("File not found or invalid request", status=400)

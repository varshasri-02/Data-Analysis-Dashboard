from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
from .utils import perform_full_analysis
import io

class CSVAnalysisSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.lower().endswith('.csv'):
            raise serializers.ValidationError('Only CSV files are allowed.')
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError('File size must be under 10MB.')
        return value

class AnalysisResultSerializer(serializers.Serializer):
    overview = serializers.DictField()
    missing_analysis = serializers.DictField()
    duplicates = serializers.DictField()
    column_summaries = serializers.DictField()
    correlation_matrix = serializers.DictField()
    outliers = serializers.DictField()
    charts = serializers.ListField(child=serializers.DictField())

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create_analysis_result(self):
        file = self.validated_data['file']
        # Read CSV
        try:
            df = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8')
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(io.BytesIO(file.read()), encoding='latin1')

        # Perform analysis
        analysis_results = perform_full_analysis(df)

        # Generate charts (simplified for API)
        charts = []
        # Add chart generation logic here if needed

        return {
            'overview': analysis_results['overview'],
            'missing_analysis': analysis_results['missing_analysis'].to_dict(),
            'duplicates': analysis_results['duplicates'],
            'column_summaries': {
                'numeric': analysis_results['column_summaries']['numeric'].to_dict() if not analysis_results['column_summaries']['numeric'].empty else {},
                'categorical': analysis_results['column_summaries']['categorical'].to_dict() if not analysis_results['column_summaries']['categorical'].empty else {}
            },
            'correlation_matrix': analysis_results['correlation_matrix'].to_dict() if not analysis_results['correlation_matrix'].empty else {},
            'outliers': analysis_results['outliers'],
            'charts': charts
        }
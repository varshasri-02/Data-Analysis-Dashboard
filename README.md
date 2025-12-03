# Data Analysis Dashboard - CSV Processing & Visualization

A production-ready Django-based web application for automated CSV data analysis with advanced visualization capabilities, REST API, and comprehensive data engineering features.

## 🚀 Features

- **Automated CSV Processing**: Upload and analyze CSV files with one-click processing
- **Data Quality Analysis**: Duplicate detection, missing value analysis, outlier detection, and data validation
- **Advanced Visualizations**: 6 different chart types including histograms, correlation heatmaps, box plots, scatter matrices, bar charts, and time series plots
- **Statistical Reports**: Comprehensive statistical summaries using Pandas
- **Export Functionality**: Export cleaned CSV, missing values reports, and correlation matrices
- **REST API**: Full DRF API with rate limiting and proper serialization
- **Security & Scalability**: File size limits, input validation, graceful handling of large datasets
- **Performance Optimized**: Processes datasets efficiently with memory management

## 🏗️ Architecture

### System Architecture Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │────│   Django App    │────│   Analysis      │
│                 │    │   (Views)       │    │   Utils         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │    │   Templates     │    │   Pandas        │
│   (DRF)         │    │   (HTML/CSS)    │    │   Matplotlib     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Storage  │    │   Database      │    │   Base64        │
│   (MEDIA_ROOT)  │    │   (SQLite)      │    │   Charts         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Request Flow
1. **Upload**: User uploads CSV → File validation → UUID filename generation → Storage in MEDIA_ROOT
2. **Analysis**: Read CSV → Perform full analysis (overview, missing values, duplicates, summaries, correlations, outliers) → Generate base64 charts
3. **Display**: Render results in template with all analysis data and visualizations
4. **Export**: Generate and download cleaned data or reports on demand

### Module-Level Explanation

#### `analysis/views.py`
- **upload_file()**: Handles file upload, validation, analysis, and result rendering
- **export_csv()**: Exports cleaned CSV data
- **export_missing_report()**: Exports missing values analysis
- **export_correlation_matrix()**: Exports correlation matrix
- **AnalyzeCSVAPIView**: REST API for programmatic analysis
- **DownloadCleanedCSVAPIView**: REST API for downloading cleaned data

#### `analysis/utils.py`
- **perform_full_analysis()**: Main analysis orchestrator with scalability checks
- **get_data_overview()**: Basic dataset statistics
- **get_missing_values_analysis()**: Comprehensive missing value detection
- **detect_duplicates()**: Duplicate row identification
- **get_column_summary()**: Separate summaries for numeric and categorical columns
- **get_correlation_matrix()**: Correlation analysis for numeric data
- **detect_outliers_iqr()**: Outlier detection using IQR method
- **clean_data()**: Data cleaning (duplicates, missing values imputation)

#### `analysis/serializers.py`
- **CSVUploadSerializer**: Validates and processes API uploads
- **AnalysisResultSerializer**: Structures API response data

#### `analysis/forms.py`
- **UploadFileForm**: Web form with file type and size validation

## 📊 Performance Metrics

- **Processing Speed**: Handles datasets up to 10MB efficiently
- **Scalability**: Graceful degradation for large datasets (>10k rows)
- **Security**: Rate limiting (10/min anon, 100/min auth), file size limits
- **Visualization Types**: 6 comprehensive charts generated in-memory
- **Error Handling**: Robust validation and user-friendly error messages

## 🛠️ Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn (Agg backend for server compatibility)
- **Database**: SQLite (production-ready with proper migrations)
- **Frontend**: HTML, CSS (Responsive Design)
- **File Handling**: UUID-based naming, MEDIA_ROOT storage, auto-cleanup

## 📈 Visualizations Generated

1. **Histograms**: Distribution analysis for numeric columns
2. **Box Plots**: Outlier visualization for numeric data
3. **Correlation Heatmap**: Relationships between numeric variables
4. **Scatter Matrix**: Pairwise relationships (for ≤4 numeric columns)
5. **Bar Charts**: Distribution of categorical variables
6. **Time Series Plots**: Trends when datetime columns detected

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/csv_analyzer.git
cd csv_analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Open your browser and navigate to `http://127.0.0.1:8000/`

## 📊 Usage

### Web Interface
1. Upload a CSV file using the web interface
2. View comprehensive data analysis results
3. Explore generated visualizations
4. Export cleaned data or reports

### REST API
```bash
# Analyze CSV
curl -X POST -F "file=@data.csv" http://127.0.0.1:8000/api/analyze/

# Download cleaned CSV
curl -X POST -F "file=@data.csv" http://127.0.0.1:8000/api/download/
```

## 🎯 What I Learned

This project provided deep insights into full-stack data engineering:

### Backend Engineering Skills
- **Django Best Practices**: Proper project structure, form validation, file handling
- **REST API Design**: DRF implementation with serializers, throttling, error handling
- **Security Implementation**: Input validation, rate limiting, file upload security
- **Scalability Considerations**: Memory management, large dataset handling, performance optimization

### Data Engineering Skills
- **Data Quality Assurance**: Comprehensive validation, cleaning, and outlier detection
- **Statistical Analysis**: Implementing industry-standard analysis methods
- **Visualization Engineering**: In-memory chart generation, base64 encoding for web delivery
- **ETL Pipeline Design**: From raw upload to cleaned export with proper error handling

### Production-Ready Features
- **Error Handling**: Graceful failure with user-friendly messages
- **File Management**: UUID naming, temporary file cleanup, MEDIA_ROOT usage
- **Performance**: Efficient pandas operations, matplotlib optimization
- **Maintainability**: Modular code structure, comprehensive documentation

## 🚀 30-Second Interview Pitch

"This Django-based CSV analyzer demonstrates full-stack data engineering expertise. It processes CSV files through a complete ETL pipeline: validation, analysis, visualization, and export. Key features include REST API with rate limiting, in-memory chart generation, outlier detection, and scalable data cleaning. Built with production best practices, it handles real-world data challenges while maintaining clean, maintainable code."

## ❓ Common Interview Questions & Answers

### Backend Architecture
**Q: How did you structure this Django application for scalability?**
A: Used modular architecture with separate utility functions, implemented proper file handling with UUIDs and auto-cleanup, added REST API with throttling, and included graceful degradation for large datasets.

**Q: What security measures did you implement?**
A: File type and size validation, rate limiting via DRF, proper error handling without information leakage, and secure file storage practices.

### Data Engineering
**Q: How do you handle missing data and outliers?**
A: Implemented comprehensive missing value analysis, IQR-based outlier detection, and automated data cleaning with median/mode imputation for different data types.

**Q: Why use base64 encoding for charts instead of file storage?**
A: Eliminates disk I/O for temporary files, reduces server storage needs, simplifies deployment, and provides immediate chart delivery in web responses.

### Performance & Scalability
**Q: How does this handle large datasets?**
A: File size limits prevent memory issues, chunked processing where applicable, graceful fallback for heavy operations on large datasets, and efficient pandas operations.

**Q: What makes this production-ready?**
A: Comprehensive error handling, input validation, security measures, modular code structure, proper Django patterns, and REST API with proper HTTP status codes.

## 💼 Backend + Data Engineering Skills Demonstrated

### Backend Engineering
- **Web Framework Expertise**: Django views, forms, templates, URL routing
- **API Development**: RESTful design with DRF, serialization, throttling
- **Security**: Input validation, rate limiting, secure file handling
- **Database Design**: Proper model relationships, migrations
- **Deployment Readiness**: Environment configuration, static/media file handling

### Data Engineering
- **Data Pipeline Construction**: ETL from upload to analysis to export
- **Quality Assurance**: Validation, cleaning, outlier detection
- **Statistical Analysis**: Comprehensive metrics and insights generation
- **Visualization Engineering**: Automated chart creation and web delivery
- **Scalability**: Memory-efficient processing, large dataset handling

This project showcases the ability to build end-to-end data applications that are both technically sound and user-friendly.

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- Pandas, NumPy
- Matplotlib, Seaborn
- Django REST Framework

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ **Star this repository** if you found it helpful!
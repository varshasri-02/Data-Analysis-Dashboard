# Data Analysis Dashboard - CSV Processing & Visualization

A Django-based web application for CSV data analysis and visualization, featuring a REST API and modular data processing pipeline.

## 🚀 Features

- **CSV Upload and Validation**: Secure file upload with type and size checks, error handling for invalid files
- **Data Analysis Pipeline**: Automated processing using Pandas for statistical summaries, missing value detection, duplicate identification, and outlier analysis
- **Visualization Generation**: Creation of charts using Matplotlib, including histograms, box plots, correlation heatmaps, scatter matrices, bar charts, and time series plots
- **Data Cleaning and Export**: Options to clean data (remove duplicates, impute missing values) and export results as CSV files
- **REST API**: Django REST Framework implementation for programmatic access with proper serialization
- **User Interface**: Clean web interface for uploading files and viewing results with responsive design

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
2. **Analysis**: Read CSV → Perform analysis (overview, missing values, duplicates, summaries, correlations, outliers) → Generate base64 charts
3. **Display**: Render results in template with analysis data and visualizations
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
- **perform_full_analysis()**: Main analysis orchestrator
- **get_data_overview()**: Basic dataset statistics
- **get_missing_values_analysis()**: Missing value detection
- **detect_duplicates()**: Duplicate row identification
- **get_column_summary()**: Summaries for numeric and categorical columns
- **get_correlation_matrix()**: Correlation analysis for numeric data
- **detect_outliers_iqr()**: Outlier detection using IQR method
- **clean_data()**: Data cleaning (duplicates, missing values imputation)

#### `analysis/serializers.py`
- **CSVUploadSerializer**: Validates and processes API uploads
- **AnalysisResultSerializer**: Structures API response data

#### `analysis/forms.py`
- **UploadFileForm**: Web form with file type and size validation

## 🛠️ Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn (Agg backend for server compatibility)
- **Database**: SQLite (with proper migrations)
- **Frontend**: HTML, CSS (Responsive Design)
- **File Handling**: UUID-based naming, MEDIA_ROOT storage, auto-cleanup

## 📊 Visualizations Generated

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
2. View data analysis results
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

This project provided insights into building a data analysis application with Django:

### Backend Engineering Skills
- **Django Structure**: Organized views, forms, models, and URL routing for clean separation of concerns
- **REST API Design**: Implemented DRF with serializers for structured data exchange
- **File Handling**: Secure upload with validation and storage management
- **Error Handling**: User-friendly error messages and graceful failure handling

### Data Engineering Skills
- **Data Processing Pipeline**: Built a modular pipeline using Pandas for analysis tasks
- **Data Quality Checks**: Implemented detection for missing values, duplicates, and outliers
- **Visualization**: Generated charts with Matplotlib and encoded for web display
- **Data Cleaning**: Applied imputation and duplicate removal techniques

### Engineering Practices
- **Modularity**: Separated concerns into utility functions and views
- **Usability**: Designed a simple interface for uploading and viewing results
- **Maintainability**: Used standard Django patterns and documented code structure

## 🚀 30-Second Interview Pitch

"This Django application processes CSV files through a data analysis pipeline: upload with validation, Pandas-based analysis for statistics and quality checks, Matplotlib visualizations, and export options. It includes a REST API and focuses on clean code structure and reliable data handling."

## ❓ Common Interview Questions & Answers

### Backend Architecture
**Q: How did you structure this Django application?**
A: The application follows Django's MTV pattern with views handling requests, forms for validation, and templates for rendering. Utility functions in utils.py encapsulate data processing logic, keeping views focused on request/response handling. The REST API uses DRF serializers for consistent data formatting.

**Q: What security measures did you implement?**
A: Implemented file type and size validation in forms, used UUID for filenames to prevent conflicts, and stored files in MEDIA_ROOT with proper permissions. Added basic rate limiting via DRF throttling.

### Data Engineering
**Q: How do you handle missing data and outliers?**
A: Used Pandas to detect missing values and applied imputation (median for numeric, mode for categorical). Outliers are detected using the IQR method on numeric columns.

**Q: Why use base64 encoding for charts?**
A: Base64 encoding allows embedding images directly in HTML responses, avoiding the need for file storage and simplifying deployment by reducing disk I/O.

### Performance & Scalability
**Q: How does this handle different dataset sizes?**
A: The application processes files in memory using Pandas, which works well for typical CSV sizes. For larger files, it relies on Pandas' efficiency, but could be extended with chunking if needed.

**Q: What makes this maintainable?**
A: Code is organized into modular functions, follows Django conventions, and includes clear separation between data processing, views, and API logic.

## 💼 Backend + Data Engineering Skills Demonstrated

### Backend Engineering
- **Web Framework Expertise**: Django views, forms, templates, URL routing
- **API Development**: RESTful design with DRF, serialization
- **File Handling**: Secure upload and storage
- **Database Design**: Basic model usage with migrations

### Data Engineering
- **Data Pipeline Construction**: ETL from upload to analysis to export
- **Quality Assurance**: Validation, cleaning, outlier detection
- **Statistical Analysis**: Basic metrics and insights
- **Visualization Engineering**: Chart creation and web delivery

This project demonstrates building a functional data analysis tool with attention to code organization and user experience.

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
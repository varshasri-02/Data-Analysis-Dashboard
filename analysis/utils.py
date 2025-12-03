import pandas as pd
import numpy as np
from typing import Dict, List, Any

def get_data_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """Get basic data overview"""
    return {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }

def get_missing_values_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze missing values"""
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    return pd.DataFrame({
        'Missing Count': missing,
        'Missing Percentage': missing_percent
    }).sort_values('Missing Count', ascending=False)

def detect_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect duplicate rows"""
    total_duplicates = df.duplicated().sum()
    duplicate_percentage = (total_duplicates / len(df)) * 100
    return {
        'total_duplicates': total_duplicates,
        'duplicate_percentage': duplicate_percentage,
        'duplicate_rows': df[df.duplicated()].head(5) if total_duplicates > 0 else pd.DataFrame()
    }

def get_column_summary(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Get summary for numeric and categorical columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    numeric_summary = df[numeric_cols].describe().T if len(numeric_cols) > 0 else pd.DataFrame()
    categorical_summary = pd.DataFrame()

    if len(categorical_cols) > 0:
        cat_data = []
        for col in categorical_cols:
            unique_count = df[col].nunique()
            most_common = df[col].mode().iloc[0] if not df[col].mode().empty else None
            most_common_count = df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
            cat_data.append({
                'Column': col,
                'Unique Values': unique_count,
                'Most Common': most_common,
                'Most Common Count': most_common_count,
                'Most Common %': (most_common_count / len(df)) * 100
            })
        categorical_summary = pd.DataFrame(cat_data)

    return {
        'numeric': numeric_summary,
        'categorical': categorical_summary
    }

def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Get correlation matrix for numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        return df[numeric_cols].corr()
    return pd.DataFrame()

def detect_outliers_iqr(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Detect outliers using IQR method"""
    if column not in df.columns or not np.issubdtype(df[column].dtype, np.number):
        return {'outliers': [], 'count': 0}

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
    return {
        'outliers': outliers.tolist(),
        'count': len(outliers),
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'percentage': (len(outliers) / len(df)) * 100
    }

def get_outliers_summary(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Get outliers summary for all numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers_summary = {}
    for col in numeric_cols:
        outliers_summary[col] = detect_outliers_iqr(df, col)
    return outliers_summary

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data: remove duplicates, handle missing values"""
    # Remove duplicates
    df_clean = df.drop_duplicates()

    # For missing values, we'll fill numeric with median, categorical with mode
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            if np.issubdtype(df_clean[col].dtype, np.number):
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            else:
                mode_val = df_clean[col].mode()
                if not mode_val.empty:
                    df_clean[col] = df_clean[col].fillna(mode_val.iloc[0])

    return df_clean

def perform_full_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform complete data analysis with scalability considerations"""
    is_large_dataset = len(df) > 10000

    result = {
        'overview': get_data_overview(df),
        'missing_analysis': get_missing_values_analysis(df),
        'duplicates': detect_duplicates(df),
        'column_summaries': get_column_summary(df),
        'cleaned_data': clean_data(df)
    }

    # For large datasets, skip heavy computations
    if not is_large_dataset:
        result['correlation_matrix'] = get_correlation_matrix(df)
        result['outliers'] = get_outliers_summary(df)
    else:
        result['correlation_matrix'] = pd.DataFrame()  # Empty for large datasets
        result['outliers'] = {'message': 'Outlier detection skipped for large datasets (>10k rows)'}

    return result
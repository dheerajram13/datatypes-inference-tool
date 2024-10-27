import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Dict, Tuple, Any
import logging

class DataTypeInferenceProcessor:
    """
    A Class to infer and convert data types in a pandas DataFrame.
    """
    
    def __init__(self, missing_values: list = None):
        self.missing_values = missing_values or ['', 'nan', 'null', 'none', 'n/a', 'na', 'not available']
        self.type_mapping = {
            'int64': 'Integer',
            'float64': 'Decimal',
            'datetime64[ns]': 'Date/Time',
            'bool': 'Boolean',
            'category': 'Category',
            'object': 'Text'
        }
        self.logger = logging.getLogger(__name__)
        
    def _is_date(self, series: pd.Series) -> bool:
        """ Check if a series contains date-like values."""
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # yyyy-mm-dd
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # m/d/yy or m/d/yyyy
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # m-d-yy or m-d-yyyy
            r'\d{2,4}\.\d{1,2}\.\d{1,2}'  # yyyy.mm.dd or yy.mm.dd
        ]
        
        sample = series.dropna().head(100)  
        for value in sample:
            if not isinstance(value, str):
                continue
            if any(re.match(pattern, value.strip()) for pattern in date_patterns):
                return True
        return False

    def _is_boolean(self, series: pd.Series) -> bool:
        """Check if a series contains boolean-like values."""
        bool_values = {'true', 'false', 'yes', 'no', 't', 'f', 'y', 'n', '1', '0'}
        sample = series.dropna().astype(str).str.lower()
        return all(val in bool_values for val in sample.unique())

    def _is_categorical(self, series: pd.Series, threshold: float = 0.5) -> bool:
        """
        Check if a series contains categorical-like values.
        """
        unique_ratio = len(series.unique()) / len(series)
        return unique_ratio < threshold and len(series.unique()) < 100

    def _convert_to_numeric(self, series: pd.Series) -> Tuple[pd.Series, str]:
        """
            Convert a series to numeric type, handling string numbers and special characters.
        """
        
        numeric_series = pd.to_numeric(series, errors='coerce')
        
        if numeric_series.notna().any():
            if numeric_series.dropna().apply(lambda x: x.is_integer()).all():
                return numeric_series.astype('Int64'), 'int64'
            return numeric_series.astype('float64'), 'float64'
            
        cleaned_series = series.astype(str).str.replace(',', '').str.replace('$', '')
        numeric_series = pd.to_numeric(cleaned_series, errors='coerce')
        
        if numeric_series.notna().any():
            if numeric_series.dropna().apply(lambda x: x.is_integer()).all():
                return numeric_series.astype('Int64'), 'int64'
            return numeric_series.astype('float64'), 'float64'
            
        return series, 'object'

    def infer_and_convert_types(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Dict[str, Any]]]:
        """
        Infer and convert column data types, returning both the converted DataFrame
        and detailed type information for each column.
        """
        converted_df = df.copy()
        column_info = {}
        
        for column in converted_df.columns:
            series = converted_df[column].replace(self.missing_values, np.nan)
            original_type = str(series.dtype)
            
            # Initialize column info
            column_info[column] = {
                'original_type': original_type,
                'inferred_type': original_type,
                'unique_values': len(series.unique()),
                'null_count': series.isna().sum(),
                'sample_values': series.dropna().head(5).tolist()
            }
            
            # Skip if series is empty or all null
            if series.isna().all():
                continue
                
            # Try date conversion first for string-like columns
            if series.dtype == 'object' and self._is_date(series):
                try:
                    converted_df[column] = pd.to_datetime(series)
                    column_info[column]['inferred_type'] = 'datetime64[ns]'
                    continue
                except (ValueError, TypeError):
                    self.logger.warning(f"Date conversion failed for column {column}")
            
            # Try boolean conversion
            if series.dtype == 'object' and self._is_boolean(series):
                try:
                    converted_df[column] = series.map({'true': True, 'false': False, 
                                                     'yes': True, 'no': False,
                                                     't': True, 'f': False,
                                                     'y': True, 'n': False,
                                                     '1': True, '0': False})
                    column_info[column]['inferred_type'] = 'bool'
                    continue
                except (ValueError, TypeError):
                    self.logger.warning(f"Boolean conversion failed for column {column}")
            
            # Try numeric conversion
            if series.dtype == 'object':
                converted_series, inferred_type = self._convert_to_numeric(series)
                if inferred_type in ('int64', 'float64'):
                    converted_df[column] = converted_series
                    column_info[column]['inferred_type'] = inferred_type
                    continue
            
            # Check for categorical
            if series.dtype == 'object' and self._is_categorical(series):
                converted_df[column] = pd.Categorical(series)
                column_info[column]['inferred_type'] = 'category'
                column_info[column]['categories'] = list(converted_df[column].cat.categories)
            
            # Update memory usage info
            column_info[column]['memory_usage'] = converted_df[column].memory_usage(deep=True)
            column_info[column]['friendly_type'] = self.type_mapping.get(
                str(converted_df[column].dtype), 'Text'
            )
        
        return converted_df, column_info

    def process_file(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Dict[str, Any]]]:
        """
        Process a CSV or Excel file and return the processed DataFrame and column information.
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, na_values=self.missing_values)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path, na_values=self.missing_values)
            else:
                raise ValueError("Unsupported file format. Please use CSV or Excel files.")
            
            return self.infer_and_convert_types(df)
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            raise
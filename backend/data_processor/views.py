from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import pandas as pd
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tempfile

@csrf_exempt
@require_http_methods(["POST"])
def process_data(request):
    if 'file' not in request.FILES:
        return JsonResponse({
            'success': False,
            'error': 'No file was uploaded'
        }, status=400)

    try:
        uploaded_file = request.FILES['file']
        
        # Check file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in ['.csv', '.xlsx', '.xls']:
            return JsonResponse({
                'success': False,
                'error': 'Invalid file format. Please upload a CSV or Excel file.'
            }, status=400)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        try:
            # Read the file based on its extension
            if file_extension == '.csv':
                df = pd.read_csv(temp_path)
            else:
                df = pd.read_excel(temp_path)

            # Process the data types
            column_info = {}
            for column in df.columns:
                column_info[column] = {
                    'original_type': str(df[column].dtype),
                    'friendly_type': infer_friendly_type(df[column]),
                    'null_count': int(df[column].isna().sum()),
                    'unique_values': int(df[column].nunique())
                }

            result = {
                'column_info': column_info,
                'row_count': len(df),
                'column_count': len(df.columns)
            }

            return JsonResponse({
                'success': True,
                'data': result
            })

        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def infer_friendly_type(series):
    """Infer a user-friendly data type from a pandas series."""
    dtype = series.dtype
    if pd.api.types.is_numeric_dtype(dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return 'Integer'
        return 'Number'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'Date/Time'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'Boolean'
    elif pd.api.types.is_categorical_dtype(dtype):
        return 'Category'
    else:
        # Check if the series could be a date
        try:
            pd.to_datetime(series)
            return 'Date/Time'
        except:
            return 'Text'
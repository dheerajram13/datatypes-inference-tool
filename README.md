# Datatypes-inference-tool

A web-based tool that helps analyze and infer data types from CSV and Excel files. This tool provides instant insights about your data structure, including column types, missing values, and unique value counts.

## Features

- 📊 Instant data type inference
- 📁 Support for CSV and Excel files
- 📈 Column analysis including:
  - Original data types
  - Inferred user-friendly types
  - Missing value counts
  - Unique value counts
- 🎯 Drag-and-drop file upload
- 💡 Interactive data preview
- 🔒 Secure file handling

## Tech Stack

### Frontend
- React
- Tailwind CSS
- Lucide React (icons)

### Backend
- Django
- Django REST Framework
- Pandas
- Python 3.8+

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/dheerajram13/datatypes-inference-tool.git
cd data-type-inference-tool
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the Django project:
```bash
cd backend
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

## Configuration

### Backend Configuration

Create a `.env` file in the backend directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Configuration

Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application

### Start the Backend Server

```bash
cd backend
python manage.py runserver
```
The backend will be available at `http://localhost:8000`

### Start the Frontend Development Server

```bash
cd frontend
npm start
# or
yarn start
```
The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Drag and drop a CSV or Excel file onto the upload area (or click to select)
3. The application will process the file and display:
   - Total number of rows and columns
   - Detailed information about each column
   - Data type information and statistics

### Sample Data

A sample CSV file is provided in the `samples` directory: `sample_customer_data.csv`

## API Documentation

### Endpoint: `/api/process-data/`

**Method:** POST

**Request:**
- Content-Type: multipart/form-data
- Body: 
  - file: CSV or Excel file

**Response:**
```json
{
    "success": true,
    "data": {
        "column_info": {
            "Name": {
                "original_type": "object",
                "friendly_type": "Text",
                "null_count": 0,
                "unique_values": 5
            },
            "Birthdate": {
                "original_type": "object",
                "friendly_type": "Date/Time",
                "null_count": 0,
                "unique_values": 5
            },
            "Score": {
                "original_type": "object",
                "friendly_type": "Text",
                "null_count": 0,
                "unique_values": 5
            },
            "Grade": {
                "original_type": "object",
                "friendly_type": "Text",
                "null_count": 0,
                "unique_values": 2
            }
        },
        "row_count": 5,
        "column_count": 4
    }
}
```

## Development

### Project Structure
```
data-type-inference-tool/
├── backend/
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── requirements.txt
│   ├── data_processor/
│   │   ├── views.py
│   │   └── data_processor.py
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── DataTypeViewer.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── sampples/
│   ├── sample-data.csv
└── README.md
```



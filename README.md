# ClinicCare Mini EMR

A lightweight Electronic Medical Records (EMR) system for managing patient consultations with ICD-10 diagnosis code support.

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite)

## Features

- 📋 **Consultation Management**: Create, view, and delete patient consultations
- 🔍 **ICD-10 Code Search**: Searchable autocomplete with 100 common diagnosis codes
- 📝 **Treatment Notes**: Detailed treatment documentation with expandable views
- 💾 **Persistent Storage**: SQLite database for reliable data storage
- 🎨 **Modern UI**: Clean, responsive interface with medical-appropriate design
- ⚡ **Fast API**: RESTful backend with automatic documentation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vue Router** - Official router for Vue.js
- **Axios** - HTTP client for API calls
- **Vite** - Next generation frontend tooling

## Project Structure

```
cliniccare-emr/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── database.py       # Database connection
│   ├── init_db.py        # Database initialization script
│   ├── requirements.txt  # Python dependencies
│   └── cliniccare.db     # SQLite database (auto-generated)
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable Vue components
│   │   ├── views/        # Page components
│   │   │   ├── ConsultationsList.vue
│   │   │   └── NewConsultation.vue
│   │   ├── router/       # Vue Router configuration
│   │   ├── services/     # API service layer
│   │   ├── App.vue       # Root component
│   │   ├── main.js       # Application entry point
│   │   └── style.css     # Global styles
│   ├── public/           # Static assets
│   ├── index.html        # HTML entry point
│   ├── package.json      # Node.js dependencies
│   └── vite.config.js    # Vite configuration
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database with ICD-10 codes:
   ```bash
   python init_db.py --force
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### Health Check
```
GET /
```
Returns API status and version information.

#### Diagnosis Codes

**Search Diagnosis Codes**
```
GET /api/diagnosis?search=<term>
```
Search ICD-10 codes by code or description (case-insensitive partial match).

| Parameter | Type   | Required | Description                |
|-----------|--------|----------|----------------------------|
| search    | string | No       | Search term                |

**Response**: Array of diagnosis codes (max 20 results)
```json
[
  {
    "id": 1,
    "code": "E11.9",
    "description": "Type 2 diabetes mellitus without complications"
  }
]
```

#### Consultations

**Create Consultation**
```
POST /api/consultation
```
Create a new patient consultation.

**Request Body**:
```json
{
  "patient_name": "John Doe",
  "diagnosis_codes": ["E11.9", "I10"],
  "treatment_notes": "Patient prescribed metformin...",
  "consultation_date": "2024-01-15T10:30:00"  // Optional
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "patient_name": "John Doe",
  "diagnosis_codes": ["E11.9", "I10"],
  "treatment_notes": "Patient prescribed metformin...",
  "consultation_date": "2024-01-15T10:30:00",
  "created_at": "2024-01-15T10:30:00"
}
```

**List Consultations**
```
GET /api/consultations?skip=0&limit=100
```
Get all consultations ordered by date descending.

| Parameter | Type    | Default | Description           |
|-----------|---------|---------|----------------------|
| skip      | integer | 0       | Records to skip      |
| limit     | integer | 100     | Max records to return|

**Response**:
```json
{
  "consultations": [...],
  "total": 50
}
```

**Get Single Consultation**
```
GET /api/consultation/{consultation_id}
```
Get a specific consultation by ID.

**Delete Consultation**
```
DELETE /api/consultation/{consultation_id}
```
Delete a consultation (returns 204 No Content).

### HTTP Status Codes

| Code | Description                  |
|------|------------------------------|
| 200  | Success                      |
| 201  | Created                      |
| 204  | No Content (successful delete)|
| 400  | Bad Request                  |
| 404  | Not Found                    |
| 422  | Validation Error             |
| 500  | Internal Server Error        |

## Database Schema

### diagnosis_codes
| Column      | Type         | Description           |
|-------------|--------------|-----------------------|
| id          | INTEGER      | Primary key           |
| code        | VARCHAR(20)  | ICD-10 code (unique)  |
| description | TEXT         | Code description      |

### consultations
| Column            | Type         | Description                |
|-------------------|--------------|----------------------------|
| id                | INTEGER      | Primary key                |
| patient_name      | VARCHAR(255) | Patient's full name        |
| diagnosis_codes   | JSON         | Array of ICD-10 codes      |
| treatment_notes   | TEXT         | Treatment documentation    |
| consultation_date | DATETIME     | Date of consultation       |
| created_at        | DATETIME     | Record creation timestamp  |

## Sample ICD-10 Codes

The system comes pre-loaded with 100 common ICD-10 codes including:

| Code    | Description                                    |
|---------|------------------------------------------------|
| E11.9   | Type 2 diabetes mellitus without complications |
| I10     | Essential (primary) hypertension               |
| J45.909 | Unspecified asthma, uncomplicated              |
| M79.3   | Panniculitis, unspecified                      |
| M54.5   | Low back pain                                  |
| F32.9   | Major depressive disorder, single episode      |
| J06.9   | Acute upper respiratory infection              |
| K21.0   | Gastro-esophageal reflux disease               |

## Development

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build
```

### Environment Variables

Backend (optional):
```bash
DATABASE_URL=sqlite:///./cliniccare.db
```

Frontend (`.env`):
```bash
VITE_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend is running on port 8000 and frontend on port 5173.

2. **Database Errors**: Re-run `python init_db.py --force` to reset the database.

3. **Port Already in Use**: 
   ```bash
   # Find and kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

4. **Module Not Found**: Ensure you've activated the virtual environment and installed dependencies.

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

# stantech_assignment
# FastAPI CRUD Application with PostgreSQL

##  Overview
This project demonstrates a **FastAPI** CRUD (Create, Read, Update, Delete) API connected to a **PostgreSQL** database using **SQLAlchemy ORM**.  
It includes error handling, testing with `pytest`.

---

## Features
- Full CRUD operations for `Items`
- PostgreSQL database with SQLAlchemy ORM
- Pydantic request & response models
- Automatic DB creation and table management
- Transaction handling
- Unit & integration testing
- Ready for Docker and production

---

## Project Structure
```
app/
├── core/
│   ├── db.py
│   └── settings.py
├── models/
│   └── testroute.py
├── routes/
│   └── testroute.py
├── tests/
│   ├── test_unit.py
│   └── test_integration.py
└── main.py
```

---

##  Setup Instructions

###  Clone the Repository
```bash
git clone https://github.com/Pradeep54199/stantech_assignment.git
cd fastapi-crud-postgres
```

### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup PostgreSQL Connection
Update your `.env` or `app/core/settings.py` with your DB credentials:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=stantech
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5️⃣ Run the Application
```bash
uvicorn app.main:app --reload
```

Then open your browser at 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

##  Testing

Run all tests using:
```bash
pytest --cov=app
```

### Example Tests
- `test_unit.py`: Unit test for logic
- `test_integration.py`: API test using `httpx`

---

##  API Endpoints

| Method | Endpoint | Description |
|--------|-----------|--------------|
| POST | `/items/` | Create a new item |
| GET | `/items/` | Retrieve all items |
| GET | `/items/{id}` | Retrieve item by ID |
| PUT | `/items/{id}` | Update an item |
| DELETE | `/items/{id}` | Delete an item |

---

##  Example Request (POST /items/)
```json
{
  "title": "First Item",
  "description": "This is a test item",
  "createdAt": "2025-11-07T10:00:00"
}
```

---

##  Tech Stack
- **FastAPI**
- **SQLAlchemy ORM**
- **PostgreSQL**
- **Pydantic**
- **Pytest**
- **Uvicorn**

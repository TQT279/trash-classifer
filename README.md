# Trash Classifier – Intelligent Waste Classification System

Trash Classifier is a web application for automated waste classification using **Deep Learning** technology.  
The backend is built with **Flask (Python)** and uses **Microsoft SQL Server** as the database.

---

## 🚀 Key Features

- **Waste Classification**  
  Identify waste types from uploaded images or a real-time camera feed.

- **User Management**  
  User registration, login, and role-based access control (**User**, **Admin**).

- **History & Statistics**  
  Store classification history and uploaded images.

- **Feedback System**  
  Users can submit feedback on classification results to help improve the model.

- **RESTful API**  
  Standard APIs for cross-platform integration.

---

## 🛠️ Tech Stack

- **Dataset**:  
  Trashbox (Kaggle)  
  https://www.kaggle.com/datasets/zzzyyy7890/trashbox

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: Microsoft SQL Server (MSSQL)
- **AI / ML**: TensorFlow, OpenCV, NumPy, Pandas
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML, CSS, JavaScript (Simple Client)

---

## 📋 Prerequisites

- Python **3.8+**
- Microsoft SQL Server
- ODBC Driver for SQL Server

---

## ⚙️ Installation

### 1. Clone or Download

Extract the source code into your working directory.

---

### 2. Install Python Dependencies

Open a terminal in the project’s root directory and run:

```bash
  pip install -r requirements.txt
```

---

### 3. Database Configuration (SQL Server)

1. Create a new database in SQL Server (e.g. `TrashClassifierDB`).
2. Run the table creation script from `sqlserver(schema).txt` to initialize the database structure.

**Tables included**:

- `users`
- `roles`
- `waste_types`
- `images`
- `classification_results`
- `feedbacks`

---

### 4. Environment Configuration

Create a `.env` file in the root directory and configure it as follows (based on `api/config.py`):

```ini
# Flask Config
FLASK_ENV=development
SECRET_KEY=your_super_secret_key_here

# Database Config
SQL_SERVER=YOUR_SQL_SERVER_NAME
SQL_DATABASE=TrashClassifierDB
SQL_USERNAME=your_db_username
SQL_PASSWORD=your_db_password
SQL_DRIVER=ODBC Driver 17 for SQL Server

# JWT Config
JWT_SECRET_KEY=your_jwt_secret_key_here

# File Upload
UPLOAD_FOLDER=uploads

# Model Paths
MODEL_PATH=models_improved/waste_model_improved_v1.h5
CLASS_INDICES_PATH=models_improved/class_indices.json

# CORS
CORS_ORIGINS=*

# Flask Server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

---

## ▶️ How to Run

The project consists of **Backend (API)** and **Client (Frontend)**.
Open **two terminal windows** to run them simultaneously.

---

### Step 1: Start the Backend Server

From the project’s root directory:

```bash
  py -m api.app
```

The API server will run at:
👉 `http://localhost:5000`

---

### Step 2: Start the Client

Open another terminal and run:

```bash
  cd client
  python -m http.server 8000
```

Access the application in your browser at:
👉 `http://localhost:8000`

---

## 📂 Project Structure

```text
trash-classifier/
├── api/                     # Flask Backend Source Code
│   ├── routes/              # API Endpoint Definitions
│   ├── services/            # Core Logic (AI model, image processing)
│   ├── app.py               # Main Application Entry Point
│   ├── config.py            # System Configuration
│   └── models.py            # Database Models Definition
├── client/                  # Frontend Source Code (HTML/CSS/JS)
├── models_improved/         # AI Model (.h5) and Label Files (.json)
├── uploads/                 # Uploaded Images Storage
├── requirements.txt         # Python Dependencies
└── sqlserver(schema).txt    # SQL Server Database Script
```

---

## 🤝 Contributing

Contributions are welcome!
Please open an **Issue** or submit a **Pull Request** if you find bugs or have improvements to suggest.

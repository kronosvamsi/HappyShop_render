# 🛒 HappyShop — E-Commerce REST API

A fully functional e-commerce backend built with **FastAPI**, **SQLAlchemy**, and **MySQL**, featuring JWT-based authentication with access and refresh token support. The React frontend is integrated and the entire application is deployed on Render.

🔗 **Live Backend API:** [https://happyshop-render.onrender.com](https://happyshop-render.onrender.com)

> **Note:** Only the backend API is deployed. Visit `/docs` for the interactive Swagger UI — [https://happyshop-render.onrender.com/docs](https://happyshop-render.onrender.com/docs)

---

## 🧰 Tech Stack

| Layer             | Technology                        |
| ----------------- | --------------------------------- |
| Backend Framework | FastAPI                           |
| ORM               | SQLAlchemy                        |
| Database          | MySQL                             |
| Authentication    | JWT (Access + Refresh Tokens)     |
| Frontend          | React                             |
| Deployment        | Render (Free Tier — Backend only) |

---

## 📁 Project Structure

```
HappyShop_render/
├── main.py              # Application entry point, app config, CORS
├── config.py            # Environment variables and settings
├── core/                # Core utilities (security, JWT, dependencies)
├── db_models/           # SQLAlchemy ORM models (database tables)
├── data_models/         # Pydantic schemas (request/response validation)
├── routes/              # API route handlers
├── services/            # Business logic layer
└── requirements.txt     # Python dependencies
```

---

## 🔐 Authentication System

The auth system uses **JWT tokens** with both access and refresh token flow:

- **Access Token** — short-lived token used to authenticate API requests
- **Refresh Token** — long-lived token used to generate a new access token without re-login
- Passwords are securely hashed before storage
- Token validation is handled via FastAPI dependency injection

### Auth Endpoints

| Method | Endpoint         | Description                                |
| ------ | ---------------- | ------------------------------------------ |
| POST   | `/auth/register` | Register a new user                        |
| POST   | `/auth/login`    | Login and receive access + refresh tokens  |
| POST   | `/auth/refresh`  | Get a new access token using refresh token |
| POST   | `/auth/logout`   | Logout and invalidate session              |

---

## 📦 API Endpoints

### Products — `/products`

| Method | Endpoint         | Description          | Auth Required |
| ------ | ---------------- | -------------------- | ------------- |
| GET    | `/products`      | Get all products     | No            |
| GET    | `/products/{id}` | Get product by ID    | No            |
| POST   | `/products`      | Create a new product | Yes           |
| PUT    | `/products/{id}` | Update a product     | Yes           |
| DELETE | `/products/{id}` | Delete a product     | Yes           |

### Categories — `/categories`

| Method | Endpoint           | Description           | Auth Required |
| ------ | ------------------ | --------------------- | ------------- |
| GET    | `/categories`      | Get all categories    | No            |
| GET    | `/categories/{id}` | Get category by ID    | No            |
| POST   | `/categories`      | Create a new category | Yes           |
| PUT    | `/categories/{id}` | Update a category     | Yes           |
| DELETE | `/categories/{id}` | Delete a category     | Yes           |

### Users — `/users`

| Method | Endpoint      | Description         | Auth Required |
| ------ | ------------- | ------------------- | ------------- |
| GET    | `/users`      | Get all users       | Yes (Admin)   |
| GET    | `/users/{id}` | Get user by ID      | Yes           |
| PUT    | `/users/{id}` | Update user profile | Yes           |
| DELETE | `/users/{id}` | Delete user         | Yes (Admin)   |

---

## 🏗️ Architecture Decisions

**Why FastAPI over Django?**
FastAPI provides automatic OpenAPI documentation, native async support, and faster performance for API-only backends. Since this project is a pure REST API consumed by a React frontend, FastAPI was a better fit than Django's more monolithic structure.

**Separation of Concerns:**
The project separates `db_models` (SQLAlchemy ORM) from `data_models` (Pydantic schemas) deliberately — this prevents tight coupling between the database layer and the API layer, making it easier to change either independently.

**Dependency Injection for Auth:**
FastAPI's `Depends()` system is used for DB session management and JWT token validation. This keeps route handlers clean and authentication reusable across endpoints.

**Access + Refresh Token Strategy:**
Using both tokens reduces security risk — short-lived access tokens limit exposure if compromised, while refresh tokens allow seamless user sessions without repeated logins.

---

## 🚀 Getting Started Locally

### Prerequisites

- Python 3.9+
- MySQL running locally

### Installation

```bash
# Clone the repository
git clone https://github.com/kronosvamsi/HappyShop_render.git
cd HappyShop_render

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/happyshop
SECRET_KEY=your_secret_key_here
DEBUG_MODE=True
DB_PASSWORD= "your db password"
```

### Run the Application

```bash
uvicorn main:app --reload
```

API will be available at: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

---

## 📄 License

This project is licensed under the MIT License.

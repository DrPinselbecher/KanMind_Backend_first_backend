
**---------------------------------- EN -----------------------------------------------**

# ✅ KANMIND – Backend (Django REST API)

**KANMIND** is a web-based management tool that helps organize tasks, boards, and teams efficiently. The **backend** provides a REST API for user management, task handling, comments, and role-based permissions.

## 🚀 Features

- User registration & login (token-based)
- Create and manage boards  
- Tasks with status, priority, due date, assignee & reviewer  
- Comments on tasks  
- Roles & permissions (board owner / members)  
- REST-based API

---

## 📦 Technologies & Requirements

| Technology              | Version / Info          |
|-------------------------|-------------------------|
| Python                  | 3.11+ (or higher)       |
| Django                  | 5.x                     |
| Django REST Framework   | 3.x                     |
| Database                | SQLite (default)        |
| Development Environment | e.g. VS Code, PyCharm   |

---

## ⚙️ Installation & Setup

### ✅ 1. Clone the FRONTEND repository

```bash
git clone https://github.com/DrPinselbecher/KanMind_Frontend
cd KanMind_Frontend
```

### ✅ 2. Clone the BACKEND repository

```bash
git clone https://github.com/DrPinselbecher/KanMind_Backend_first_backend
cd KanMind_Backend
```

### ✅ 3. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```
### ✅ 4. Install dependencies

```bash
pip install -r requirements.txt
```
---

## ▶️ Start project


### 👉 1. Run database migrations:

```bash
python manage.py migrate
```
### 👉 2. Create admin user (optional):

```bash
python manage.py createsuperuser
```
### 👉 3. Start the server:

```bash
python manage.py runserver
```
---

## 📄 Requirements (requirements.txt)

```bash
asgiref==3.8.1
Django==5.1.6
djangorestframework==3.16.1
sqlparse==0.5.3
tzdata==2025.1
```
---

## 👤 Autor

Project: KANMIND
Developer: René Theis
GitHub: https://github.com/DrPinselbecher

---

## 📌 Notes

The **Backend** run here:
👉 http://127.0.0.1:8000/
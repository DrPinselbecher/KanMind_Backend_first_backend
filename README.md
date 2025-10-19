
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

Projekt: KANMIND
Entwickler: Dein Name
GitHub: https://github.com/DrPinselbecher

---

## 📌 Notes

Das **Backend** läuft hier:
👉 http://127.0.0.1:8000/



**---------------------------------- DE -----------------------------------------------**



# DE ✅ KANMIND – Backend (Django REST API)

**KANMIND** ist ein webbasiertes Management-Tool, mit dem Aufgaben, Boards und Teams effizient organisiert werden können. Das **Backend** stellt eine REST API bereit für Benutzerverwaltung, Aufgabenmanagement, Kommentare und Rollenrechte.


## 🚀 Funktionen

- Benutzerregistrierung & Login (Token basiert)
- Boards erstellen und verwalten  
- Aufgaben (Tasks) mit Status, Priorität, Fälligkeit, Assignee & Reviewer  
- Kommentare zu Aufgaben  
- Rechte & Rollen (Board-Owner / Mitglieder)  
- API basiert (REST)

---

## 📦 Technologien & Voraussetzungen

| Technologie           | Version / Info         |
|-----------------------|------------------------|
| Python                | 3.11+ (oder höher)     |
| Django                | 5.x                    |
| Django REST Framework | 3.x                    |
| Datenbank             | SQLite (Standard)      |
| Entwicklungsumgebung  | z. B. VS Code, PyCharm |

---

## ⚙️ Installation & Setup

### ✅ 1. Repository klonen FRONTEND

```bash
git clone https://github.com/DrPinselbecher/KanMind_Frontend
cd KanMind_Frontend
```

### ✅ 2. Repository klonen BACKEND

```bash
git clone https://github.com/DrPinselbecher/KanMind_Backend_first_backend
cd KanMind_Backend
```

### ✅ 3. Virtuelle Umgebung erstellen & aktivieren

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```
### ✅ 4. Dependencies installieren

```bash
pip install -r requirements.txt
```
---

## ▶️ Projekt starten


### 👉 1. Datenbank migrieren:

```bash
python manage.py migrate
```
### 👉 2. Admin-Benutzer anlegen (optional):

```bash
python manage.py createsuperuser
```
### 👉 3. Server starten:

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

Projekt: KANMIND
Entwickler: Dein Name
GitHub: https://github.com/DrPinselbecher

---

## 📌 Hinweise

Das **Frontend** findest du hier:  
👉 https://github.com/DrPinselbecher/KanMind_Frontend

Das **Backend** läuft hier:
👉 http://127.0.0.1:8000/
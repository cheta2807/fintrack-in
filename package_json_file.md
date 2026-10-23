# 🪙 FinTrack.in — Personal Finance & Automated Analytics Engine

A full-stack, data-driven personal finance tracking application optimized for Indian Rupee (₹ INR) currency formats, automated portfolio analytics, rule-based financial advice, and spending heuristics.

## 🌟 Key Features

* **📊 Visual Analytics Dashboard:** Real-time cash flow trends, category breakdown charts, and budget utilization metrics built with **Recharts**.

* **🇮🇳 Localized for India (₹ INR):** Pre-configured with Indian Rupee formatting (`₹1,50,000`), UPI payment modes, Zerodha SIP tracking, and metro rent expense heuristics.

* **⚡ FastAPI REST Backend:** Asynchronous Python API endpoints for transactional CRUD, CSV statement exports, and summary stats.

* **🐘 PostgreSQL Relational Schema:** Production-grade database layout with cascade rules, custom constraints, and composite indexes.

* **🐼 Pandas Analytics Engine:** Data pipeline routine that evaluates liquid surplus, 6-month emergency reserve targets, and budget category overruns.

* **🤖 Rule-Based Advisory Engine:** Algorithmic heuristics for savings velocity rate, discretionary burn rate, and investment target checks.

## 🏗️ System Architecture

```
                       ┌─────────────────────────┐
                       │   React + Tailwind UI   │
                       │   (Recharts & Lucide)   │
                       └────────────┬────────────┘
                                    │  HTTP / JSON
                                    ▼
                       ┌─────────────────────────┐
                       │    FastAPI REST API     │
                       └────────────┬────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               │                                         │
               ▼                                         ▼
┌─────────────────────────────┐           ┌─────────────────────────────┐
│    PostgreSQL Database      │           │   Pandas Data Analytics     │
│   (Relational Ledger)       │           │   (Heuristics Pipeline)     │
└─────────────────────────────┘           └─────────────────────────────┘

```

## 📂 Repository Structure

```
personal-finance-tracker/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── analytics.py
│   │   │       │   └── transactions.py
│   │   │       └── api.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   └── transaction.py
│   │   ├── schemas/
│   │   │   └── transaction.py
│   │   ├── services/
│   │   │   └── analytics.py
│   │   └── main.py
│   ├── database/
│   │   └── schema.sql
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md

```

## 🚀 Quick Start Guide

### Prerequisites

* Python 3.10+

* Node.js 18+ & `npm`

* PostgreSQL 14+ (or Docker)

### 1. Backend Setup (FastAPI + PostgreSQL)

```
# Clone the repository
git clone https://github.com/your-username/personal-finance-tracker.git
cd personal-finance-tracker/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database schema
psql -U postgres -d fin_db -f database/schema.sql

# Start backend server
uvicorn app.main:app --reload

```

The API will be available at `http://localhost:8000`. Interactive docs available at `http://localhost:8000/docs`.

### 2. Frontend Setup (React + Vite)

```
cd ../frontend

# Install node dependencies
npm install

# Start development server
npm run dev

```

Open `http://localhost:5173` in your browser.

## 🗄️ Database Schema Sample (`database/schema.sql`)

```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    preferred_currency VARCHAR(10) DEFAULT 'INR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    type VARCHAR(10) CHECK (type IN ('Income', 'Expense')),
    category VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT NOT NULL,
    payment_method VARCHAR(30) DEFAULT 'UPI',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tx_user_date ON transactions(user_id, transaction_date DESC);

```

## 💻 Tech Stack

* **Frontend:** React, Tailwind CSS, Lucide Icons, Recharts, Vite

* **Backend:** FastAPI, Pydantic, SQLAlchemy, Pandas

* **Database:** PostgreSQL

* **DevOps:** Uvicorn, Docker-ready, GitHub Actions

## 📄 License

This project is licensed under the [MIT License](LICENSE).
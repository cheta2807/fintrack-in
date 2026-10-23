-- ========================================================
-- FinTrack.in PostgreSQL Relational Schema Script
-- ========================================================

DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    preferred_currency VARCHAR(10) DEFAULT 'INR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Transactions Table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    type VARCHAR(10) NOT NULL CHECK (type IN ('Income', 'Expense')),
    category VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT NOT NULL,
    payment_method VARCHAR(30) DEFAULT 'UPI',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Budgets Table
CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    amount_limit NUMERIC(12, 2) NOT NULL CHECK (amount_limit > 0),
    UNIQUE(user_id, category)
);

-- Indexes for performance
CREATE INDEX idx_tx_user_date ON transactions(user_id, transaction_date DESC);
CREATE INDEX idx_tx_category ON transactions(category);

-- Seed Initial User
INSERT INTO users (id, email, full_name, preferred_currency) 
VALUES (1, 'dev.engineer@fintrack.in', 'Vikram Sharma', 'INR');

-- Seed Initial Transactions (INR)
INSERT INTO transactions (user_id, amount, type, category, transaction_date, description, payment_method) VALUES
(1, 145000.00, 'Income', 'Salary', '2026-10-01', 'Tech Salary (Infosys)', 'Bank Transfer'),
(1, 32000.00, 'Expense', 'Housing', '2026-10-02', 'House Rent - HSR Layout', 'UPI'),
(1, 6450.00, 'Expense', 'Groceries', '2026-10-03', 'Zepto & Instamart Groceries', 'Credit Card'),
(1, 35000.00, 'Income', 'Freelance', '2026-10-05', 'Freelance AI Consulting', 'Bank Transfer'),
(1, 3200.00, 'Expense', 'Utilities', '2026-10-08', 'Bescom Electricity & Water', 'UPI'),
(1, 4800.00, 'Expense', 'Dining Out', '2026-10-10', 'Dinner at Toit Brewpub', 'Credit Card'),
(1, 25000.00, 'Expense', 'Investments', '2026-10-12', 'Zerodha Mutual Fund SIP', 'Auto-Debit'),
(1, 2500.00, 'Expense', 'Transportation', '2026-10-14', 'Fuel / Petrol Filling', 'Fastag / UPI'),
(1, 12400.00, 'Expense', 'Shopping', '2026-10-18', 'Amazon Festival Shopping', 'Credit Card');
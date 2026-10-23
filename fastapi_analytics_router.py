from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import pandas as pd
from app.db.session import get_db
from app.models.transaction import Transaction

router = APIRouter()

@router.get("/summary")
def get_financial_summary(
    user_id: int = Query(1, description="ID of the user"),
    month: Optional[str] = Query(None, description="Format YYYY-MM"),
    db: Session = Depends(get_db)
):
    """
    Computes summary metrics (Total Income, Total Expense, Net Balance, Savings Velocity)
    for Indian household portfolios using Pandas dataframe operations.
    """
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    transactions = query.all()

    if not transactions:
        return {
            "currency": "INR (₹)",
            "total_income": 0.0,
            "total_expense": 0.0,
            "net_balance": 0.0,
            "savings_velocity_pct": 0.0,
            "income_count": 0,
            "expense_count": 0
        }

    # Convert SQLAlchemy query result to Pandas DataFrame
    data = [{
        "id": t.id,
        "amount": float(t.amount),
        "type": t.type,
        "category": t.category,
        "date": str(t.transaction_date)
    } for t in transactions]
    
    df = pd.DataFrame(data)

    if month:
        df = df[df['date'].str.startswith(month)]

    income = float(df[df['type'] == 'Income']['amount'].sum()) if 'Income' in df['type'].values else 0.0
    expense = float(df[df['type'] == 'Expense']['amount'].sum()) if 'Expense' in df['type'].values else 0.0
    net_balance = income - expense
    
    savings_velocity = ((income - expense) / income * 100) if income > 0 else 0.0

    return {
        "currency": "INR (₹)",
        "total_income": round(income, 2),
        "total_expense": round(expense, 2),
        "net_balance": round(net_balance, 2),
        "savings_velocity_pct": round(savings_velocity, 2),
        "income_count": int(len(df[df['type'] == 'Income'])),
        "expense_count": int(len(df[df['type'] == 'Expense']))
    }

@router.get("/heuristics")
def get_ai_heuristics(
    user_id: int = Query(1),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Evaluates rule-based financial indicators:
    - Emergency Fund threshold (6x monthly expenses)
    - High surplus allocation checks
    - Discretionary cost center risks
    """
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        return {"alerts": [], "recommendations": []}

    df = pd.DataFrame([{
        "amount": float(t.amount),
        "type": t.type,
        "category": t.category
    } for t in transactions])

    expenses_df = df[df['type'] == 'Expense']
    total_expense = expenses_df['amount'].sum() if not expenses_df.empty else 0.0
    
    category_breakdown = expenses_df.groupby('category')['amount'].sum().to_dict() if not expenses_df.empty else {}

    alerts = []
    recs = []

    # Check emergency buffer
    ideal_emergency_fund = total_expense * 6
    recs.append({
        "title": "Emergency Fund Buffer Threshold",
        "description": f"Based on recurring monthly burn rate of ₹{total_expense:,.0f}, your target 6-month reserve is ₹{ideal_emergency_fund:,.0f}."
    })

    # Category overload checks
    for cat, val in category_breakdown.items():
        if val > 10000 and cat in ['Dining Out', 'Shopping']:
            alerts.append({
                "severity": "WARNING",
                "category": cat,
                "message": f"High discretionary burn rate detected in '{cat}' (₹{val:,.0f}). Consider capping weekend spending."
            })

    return {
        "alerts": alerts,
        "recommendations": recs,
        "emergency_buffer_inr": ideal_emergency_fund
    }
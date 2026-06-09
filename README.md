# VaultView 💰

VaultView is a Personal Finance Tracker built using Python. It helps users manage income, expenses, savings, and investments through an intuitive web-based dashboard.

## Features

- Secure User Authentication
- Password Hashing using bcrypt
- Income and Expense Tracking
- Interactive Dashboard
- Financial Reports and Analytics
- Expense Breakdown Charts
- Monthly Income vs Expense Analysis
- Savings Rate Visualization
- Transaction History Filtering
- CSV Export Functionality

## Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- bcrypt

## Project Structure

```
VaultView/
│
├── app.py
│
├── db/
│   └── database.py
│
├── utils/
│   └── auth.py
│
├── views/
│   ├── dashboard.py
│   ├── transactions.py
│   ├── reports.py
│   └── history.py
│
└── requirements.txt
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/VaultView.git
cd VaultView
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

## Database Design

### Users Table

| Field | Type |
|---------|---------|
| id | INTEGER |
| username | TEXT |
| password | TEXT |

### Transactions Table

| Field | Type |
|---------|---------|
| id | INTEGER |
| user_id | INTEGER |
| type | TEXT |
| category | TEXT |
| amount | REAL |
| note | TEXT |
| date | TEXT |

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- Parameterized SQL queries
- Input validation

## Future Enhancements

- Budget Goal Tracking
- Recurring Transactions
- AI Spending Insights
- Financial Forecasting
- Multi-Currency Support
- Cloud Database Integration

## Author

Sri Nandana Bekkem

AI & DS Department

Stanley College of Engineering and Technology for Women

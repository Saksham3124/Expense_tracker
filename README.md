# 💰 Expense Tracker (AI-Powered)

A modern **AI-assisted expense tracking web application** built with **Django, Tailwind CSS, and Chart.js**.
It helps users manage expenses, track spending patterns, set budgets, and get intelligent insights into their financial behavior.

---

# 🚀 Features

### 📊 Smart Dashboard

* Overview of total expenses
* Monthly spending summary
* Spending analytics
* Recent expenses table

### 🤖 AI Expense Categorization

* Predicts category based on description
* Machine learning model trained from past expenses
* Suggests category before saving

### 📈 Expense Prediction

* Predicts next month’s spending based on historical data
* Helps users plan budgets

### 📉 Budget Alerts

* Set category budgets
* Alerts when spending exceeds budget

### 📊 Interactive Charts

* Spending by category (Pie chart)
* Monthly spending trend (Line chart)

### 🌓 Dark / Light Mode

* Theme toggle
* Theme saved using local storage

### 📱 Mobile Responsive

* Works smoothly on phones and tablets
* Responsive navigation and layout

### ⚡ Modern UI

* Tailwind CSS styling
* Animated components
* Toast notifications
* Page loader

---
## 📸 Screenshots

### 🏠 Dashboard
<p align="center">
  <img src="screenshots/dashboard.png" width="800">
</p>

### ➕ Add Expense
<p align="center">
  <img src="screenshots/add_expense.png" width="800">
</p>

### 📂 Categories
<p align="center">
  <img src="screenshots/categories.png" width="800">
</p>

### 📋 Expense List
<p align="center">
  <img src="screenshots/list.png" width="800">
</p>

### 🔐 Login Page
<p align="center">
  <img src="screenshots/login.png" width="500">
</p>

---


# 🛠 Tech Stack

Frontend

* HTML
* Tailwind CSS
* JavaScript
* Chart.js

Backend

* Django
* Python

Machine Learning

* Scikit-learn
* Naive Bayes text classification

Database

* SQLite (default)
* PostgreSQL (recommended for production)

---

# 📂 Project Structure

```
expense_tracker/
│
├── expenses/              # Main app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── ml_model.py        # AI prediction model
│   ├── urls.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── add_expense.html
│   ├── expense_list.html
│
├── static/
│
├── manage.py
└── requirements.txt
```

---

# ⚙️ Installation

Clone the repository

```
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run migrations

```
python manage.py migrate
```

Create admin user

```
python manage.py createsuperuser
```

Run server

```
python manage.py runserver
```

Open in browser

```
http://127.0.0.1:8000
```

---

# 📊 AI Category Prediction

The project includes a **machine learning model** that learns from past expenses.

It uses:

* TF-IDF vectorization
* Multinomial Naive Bayes classifier

Example predictions

| Description      | Predicted Category |
| ---------------- | ------------------ |
| Uber ride        | Transport          |
| Swiggy order     | Food               |
| Amazon purchase  | Entertainment      |
| Electricity bill | Bills              |

---

# 🌍 Deployment

The project can be deployed easily using:

* Render
* Railway
* DigitalOcean
* AWS

Production server example:

```
gunicorn expense_tracker.wsgi
```

---

# 🔐 Security Features

* CSRF protection
* Secure authentication
* Budget validation
* Form validation

---

# 📌 Future Improvements

* Expense receipt scanning
* AI financial recommendations
* Multi-user family budgeting
* Export reports (PDF / Excel)
* Mobile app version

---

# 👨‍💻 Author

Saksham

B.Tech Student – BIT Mesra

---

# ⭐ If you like this project

Give it a star on GitHub ⭐

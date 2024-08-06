# Expense Tracking App

This project is an Expense Tracking App built with Flask and MySQL, allowing users to register, log in, and manage their expenses and income with a user-friendly interface. It includes features for viewing summaries, recent transactions, and adding new expenses and income.

## Features
- User Registration and Login
- Dashboard displaying total earnings, total expenses, net balance, and total transactions
- Forms for adding new expenses and income
- Tables for viewing recent expenses and income

## Technologies Used
- Flask
- MySQL
- SQLAlchemy
- Bootstrap

## Setup and Installation
1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Configure your MySQL database in `main.py`
4. Run the application: `flask run`

## Project Structure
- `main.py`: Main application file
- `templates/`: Contains HTML templates (`login.html`, `register.html`, `home.html`)
- `static/css/`: Contains CSS file (`style.css`)
- `models.py`: Contains SQLAlchemy models (`Users`, `Expense`, `Income`)

## Usage
1. Register a new user or log in with existing credentials.
2. Add new expenses and income using the provided forms.
3. View your financial summaries and recent transactions on the dashboard.


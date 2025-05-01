from flask import Flask, render_template, request, redirect, url_for
import datetime
import functools # For total calculation

app = Flask(__name__)

# --- Data Storage (In-Memory) ---
# We'll use a list of dictionaries to store expenses.
# Each dictionary will represent one expense.
# NOTE: This data will be lost when the app stops. See "Next Steps" for persistence.
expenses = [
    {'id': 1, 'description': 'Groceries', 'amount': 35.50, 'category': 'Food', 'date': datetime.date(2023, 10, 26)},
    {'id': 2, 'description': 'Gasoline', 'amount': 55.00, 'category': 'Transport', 'date': datetime.date(2023, 10, 25)},
    {'id': 3, 'description': 'Movie Tickets', 'amount': 25.00, 'category': 'Entertainment', 'date': datetime.date(2023, 10, 24)}
]
# Simple counter for unique IDs
next_id = 4

# --- Helper Function ---
def get_total_expenses(expense_list):
  """Calculates the total amount from a list of expense dictionaries."""
  # Using functools.reduce for a functional approach (or a simple loop works too)
  # return functools.reduce(lambda total, expense: total + expense['amount'], expense_list, 0)
  # Simpler loop version:
  total = 0
  for expense in expense_list:
      total += expense['amount']
  return total

# --- Routes ---

# Route 1: View All Expenses & Add Expense Form (Homepage)
@app.route('/')
def index():
    """Displays all expenses and the form to add new ones."""
    # Sort expenses by date (most recent first)
    sorted_expenses = sorted(expenses, key=lambda x: x['date'], reverse=True)
    total_expenses = get_total_expenses(expenses)
    return render_template('index.html', expenses=sorted_expenses, total_expenses=total_expenses)

# Route 2: Handle Adding a New Expense
@app.route('/add', methods=['POST'])
def add_expense():
    """Processes the form submission and adds a new expense."""
    global next_id # Use the global counter

    description = request.form['description']
    amount_str = request.form['amount']
    category = request.form['category']
    date_str = request.form['date'] # Date comes as string 'YYYY-MM-DD'

    # Basic Validation
    if not description or not amount_str or not category or not date_str:
        # Ideally, add flash messages to inform the user about the error
        print("Error: Missing form fields")
        return redirect(url_for('index')) # Redirect back if invalid

    try:
        amount = float(amount_str)
        expense_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        # Handle invalid amount or date format
        print("Error: Invalid amount or date format")
        return redirect(url_for('index'))

    new_expense = {
        'id': next_id,
        'description': description,
        'amount': amount,
        'category': category,
        'date': expense_date
    }
    expenses.append(new_expense)
    next_id += 1 # Increment the ID for the next one

    return redirect(url_for('index')) # Redirect back to the homepage

# Route 3: Delete an Expense
@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    """Deletes an expense based on its ID."""
    global expenses # We need to modify the global list
    # Use a list comprehension to create a new list excluding the expense to delete
    expenses = [expense for expense in expenses if expense['id'] != expense_id]
    return redirect(url_for('index'))

# Route 4: View Expenses by Category (Example)
# You could make this more dynamic (e.g., dropdown selection)
@app.route('/category/<string:category_name>')
def view_by_category(category_name):
    """Displays expenses filtered by a specific category."""
    filtered_expenses = [expense for expense in expenses if expense['category'].lower() == category_name.lower()]
    total_filtered = get_total_expenses(filtered_expenses)
    # We can reuse the main index template
    return render_template('index.html',
                           expenses=filtered_expenses,
                           total_expenses=total_filtered,
                           filter_title=f"Expenses for Category: {category_name.capitalize()}") # Pass a title

# --- Run the App ---
if __name__ == '__main__':
    # debug=True allows auto-reloading during development and shows detailed errors
    # **Do not use debug=True in a production environment!**
    app.run(debug=True)
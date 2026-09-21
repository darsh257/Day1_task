import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def get_expenses():
    """Return all private expense records."""

    with open(DATA_DIR / "expenses.json", "r") as file:
        expenses = json.load(file)

    return expenses


def get_budgets():
    """Return the user's private budget information."""

    with open(DATA_DIR / "budget.json", "r") as file:
        budget = json.load(file)

    return budget


def calculate_category_totals(expenses):
    """Calculate total spending for every category."""

    totals = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category not in totals:
            totals[category] = 0

        totals[category] += amount

    return totals


def compare_budgets(totals, budget):
    """Compare spending against the user's budget."""

    results = {}

    for category, spent in totals.items():

        category_budget = budget.get(category, 0)

        difference = spent - category_budget

        if difference > 0:
            status = "OVER BUDGET"
        else:
            status = "WITHIN BUDGET"

        results[category] = {
            "spent": spent,
            "budget": category_budget,
            "difference": difference,
            "status": status
        }

    return results
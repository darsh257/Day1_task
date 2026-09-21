import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_expenses():
    with open(DATA_DIR / "expenses.json", "r") as file:
        return json.load(file)


def load_budget():
    with open(DATA_DIR / "budget.json", "r") as file:
        return json.load(file)


def calculate_category_totals(expenses):

    totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        totals[category] = totals.get(category, 0) + amount

    return totals


def compare_with_budget(totals, budget):

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


def run_workflow():

    print()
    print("=" * 72)
    print("                      RULE-BASED WORKFLOW")
    print("=" * 72)

    # --------------------------------------------------
    # STEP 1
    # --------------------------------------------------

    print("\n[STEP 1] LOAD PRIVATE EXPENSE DATA")
    print("-" * 72)

    expenses = load_expenses()

    print(f"Expense records loaded : {len(expenses)}")

    # --------------------------------------------------
    # STEP 2
    # --------------------------------------------------

    print("\n[STEP 2] LOAD BUDGET DATA")
    print("-" * 72)

    budget = load_budget()

    print(f"Budget categories      : {len(budget)}")

    # --------------------------------------------------
    # STEP 3
    # --------------------------------------------------

    print("\n[STEP 3] CALCULATE CATEGORY TOTALS")
    print("-" * 72)

    totals = calculate_category_totals(expenses)

    print(f"{'CATEGORY':<20}{'TOTAL SPENT':>15}")
    print("-" * 35)

    for category, amount in totals.items():
        print(f"{category:<20}{'₹' + str(amount):>15}")

    # --------------------------------------------------
    # STEP 4
    # --------------------------------------------------

    print("\n[STEP 4] APPLY PREDEFINED BUDGET RULES")
    print("-" * 72)

    results = compare_with_budget(totals, budget)

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    print("\n" + "=" * 72)
    print("                         FINAL RESULT")
    print("=" * 72)

    print(
        f"{'CATEGORY':<18}"
        f"{'SPENT':>12}"
        f"{'BUDGET':>12}"
        f"{'DIFFERENCE':>15}"
        f"  STATUS"
    )

    print("-" * 72)

    for category, data in results.items():

        difference = data["difference"]

        if difference > 0:
            difference_text = f"+₹{difference}"
        else:
            difference_text = f"-₹{abs(difference)}"

        print(
            f"{category:<18}"
            f"{'₹' + str(data['spent']):>12}"
            f"{'₹' + str(data['budget']):>12}"
            f"{difference_text:>15}"
            f"  {data['status']}"
        )

    print("-" * 72)

    over_budget = [
        category
        for category, data in results.items()
        if data["status"] == "OVER BUDGET"
    ]

    within_budget = [
        category
        for category, data in results.items()
        if data["status"] == "WITHIN BUDGET"
    ]

    print("\n[SUMMARY]")
    print(f"Over budget   : {', '.join(over_budget)}")
    print(f"Within budget : {', '.join(within_budget)}")

    print("\n[WORKFLOW CHARACTERISTICS]")
    print("-" * 72)
    print("Private data access : YES")
    print("LLM usage           : NO")
    print("Tool selection      : NO")
    print("Decision mechanism  : PREDEFINED RULES")
    print("Execution path      : FIXED")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    run_workflow()
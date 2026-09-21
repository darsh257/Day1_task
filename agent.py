import os
import json

from dotenv import load_dotenv
from groq import Groq

from tools import (
    get_expenses,
    get_budgets,
    calculate_category_totals,
    compare_budgets
)


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ==========================================================
# TOOL DEFINITIONS
# ==========================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_expenses",
            "description": "Get the user's private expense records.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_budgets",
            "description": "Get the user's private category budgets.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_category_totals",
            "description": "Calculate total spending for each category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expenses": {
                        "type": "array"
                    }
                },
                "required": ["expenses"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "compare_budgets",
            "description": "Compare spending against category budgets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "totals": {
                        "type": "object"
                    },
                    "budget": {
                        "type": "object"
                    }
                },
                "required": ["totals", "budget"]
            }
        }
    }
]


# ==========================================================
# TOOL EXECUTION
# ==========================================================

def execute_tool(tool_name, arguments):

    if tool_name == "get_expenses":
        return get_expenses()

    if tool_name == "get_budgets":
        return get_budgets()

    if tool_name == "calculate_category_totals":
        return calculate_category_totals(
            arguments["expenses"]
        )

    if tool_name == "compare_budgets":
        return compare_budgets(
            arguments["totals"],
            arguments["budget"]
        )

    raise ValueError(f"Unknown tool: {tool_name}")


# ==========================================================
# STRUCTURED OBSERVATION
# ==========================================================

def display_observation(tool_name, result):

    print("\n    OBSERVATION")
    print("    " + "-" * 56)

    if tool_name == "get_expenses":

        print(
            f"    Retrieved {len(result)} private expense records."
        )

    elif tool_name == "get_budgets":

        print(
            f"    {'CATEGORY':<18}{'BUDGET':>12}"
        )

        for category, amount in result.items():
            print(
                f"    {category:<18}{'₹' + str(amount):>12}"
            )

    elif tool_name == "calculate_category_totals":

        print(
            f"    {'CATEGORY':<18}{'SPENT':>12}"
        )

        for category, amount in result.items():
            print(
                f"    {category:<18}{'₹' + str(amount):>12}"
            )

    elif tool_name == "compare_budgets":

        print(
            f"    {'CATEGORY':<18}"
            f"{'SPENT':>10}"
            f"{'BUDGET':>10}"
            f"{'DIFFERENCE':>14}"
        )

        for category, data in result.items():

            difference = data["difference"]

            if difference > 0:
                difference_text = f"+₹{difference}"
            else:
                difference_text = f"-₹{abs(difference)}"

            print(
                f"    {category:<18}"
                f"₹{data['spent']:>8}"
                f"₹{data['budget']:>8}"
                f"{difference_text:>14}"
            )

        print()

        for category, data in result.items():
            print(
                f"    {category:<18}"
                f"{data['status']}"
            )

    print("    " + "-" * 56)


# ==========================================================
# AI AGENT LOOP
# ==========================================================

def run_agent(user_question):

    messages = [

        {
            "role": "system",
            "content": """
You are an AI agent for analyzing a student's private
expense and budget information.

Private data is available only through tools.

Your job is to:

1. Understand the user's request.
2. Select the appropriate tool.
3. Execute the tool.
4. Observe the result.
5. Decide whether another tool is required.
6. Continue until enough information is available.
7. Produce a final answer.

Do not invent private financial information.
"""
        },

        {
            "role": "user",
            "content": user_question
        }
    ]

    step = 1

    while True:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=messages,

            tools=TOOLS,

            tool_choice="auto",

            temperature=0.1
        )

        assistant_message = response.choices[0].message

        # --------------------------------------------------
        # FINAL ANSWER
        # --------------------------------------------------

        if not assistant_message.tool_calls:

            print("\n" + "=" * 72)
            print("                         FINAL ANSWER")
            print("=" * 72)

            print(assistant_message.content)

            print("\n" + "-" * 72)
            print("[AGENT SUMMARY]")
            print("-" * 72)

            print("Private data access : THROUGH TOOLS")
            print("LLM                 : openai/gpt-oss-20b")
            print("Tool calls          :", step - 1)
            print("Loop status         : COMPLETED")

            print("=" * 72)

            return

        # Add assistant tool request to conversation
        messages.append(assistant_message)

        # --------------------------------------------------
        # TOOL EXECUTION
        # --------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments or "{}"
            )

            print("\n" + "-" * 72)
            print(f"[STEP {step}]")
            print("-" * 72)

            print(f"TOOL SELECTED : {tool_name}")

            # Don't print huge JSON arguments
            if tool_name == "get_expenses":
                print("INPUT         : No arguments")

            elif tool_name == "get_budgets":
                print("INPUT         : No arguments")

            elif tool_name == "calculate_category_totals":

                count = len(
                    arguments.get("expenses", [])
                )

                print(
                    f"INPUT         : {count} expense records"
                )

            elif tool_name == "compare_budgets":

                count = len(
                    arguments.get("totals", {})
                )

                print(
                    f"INPUT         : {count} categories"
                )

            # Execute tool
            result = execute_tool(
                tool_name,
                arguments
            )

            # Display clean observation
            display_observation(
                tool_name,
                result
            )

            # Send observation back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )

            step += 1


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    question = """
Analyze my spending this month.

Tell me:

1. How much I spent in each category.
2. Which categories are over budget.
3. How much I exceeded each budget by.
4. Which categories are still within budget.
"""

    print()
    print("=" * 72)
    print("                           AI AGENT")
    print("=" * 72)

    print("\n[USER REQUEST]")
    print("-" * 72)
    print(question)

    print("\n[AGENT EXECUTION]")

    run_agent(question)
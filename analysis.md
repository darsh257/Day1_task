# Day 1 — Plain Chatbot vs Rule-Based Workflow vs AI Agent

## 1. Scenario

This project uses a **student expense and budget analysis** scenario. Private expense records and monthly budgets are stored locally in JSON files. The user asks the system to calculate spending by category, identify over-budget categories, and show the difference from the budget.

---

## 2. Plain Chatbot

The plain chatbot uses only an **LLM** to understand the user's request and generate a response. It has no access to the private expense or budget files and does not use any tools.

Therefore, when asked to analyze the user's actual spending, it explains that it cannot access the required private data. It can provide general advice but cannot calculate the user's real expenses.

**Architecture:**

```text
User → LLM → Response
```

**Limitation:** No private-data access or external tool usage.

---

## 3. Rule-Based Workflow

The rule-based workflow does not use an LLM. It directly reads the private JSON files and follows a predefined sequence:

```text
Load Expenses
      ↓
Load Budget
      ↓
Calculate Totals
      ↓
Compare With Budget
      ↓
Generate Report
```

For the sample data, Food and Entertainment are over budget, while Transport and Education are within budget.

This approach is predictable and reliable for predefined tasks, but it is less flexible because every possible operation must be programmed in advance.

**Limitation:** Fixed execution path and limited flexibility.

---

## 4. AI Agent

The AI agent combines an **LLM + Tools + Loop**.

The available tools allow the agent to retrieve expenses, retrieve budgets, calculate category totals, and compare spending with budgets.

The agent dynamically selects tools, receives their results as observations, and continues until it has enough information to answer the user.

```text
User Request
     ↓
LLM
     ↓
Select Tool
     ↓
Execute Tool
     ↓
Observe Result
     ↓
LLM
     ↓
Next Tool / Final Answer
```

In this project, the agent retrieves the private data, calculates the totals, compares them with the budgets, and generates the final response.

**Limitation:** More flexible but depends on correct LLM tool selection and therefore requires proper validation and error handling.

---

## 5. Comparison

| Basis               | Plain Chatbot            | Rule-Based Workflow  | AI Agent                      |
| ------------------- | ------------------------ | -------------------- | ----------------------------- |
| Flexibility         | Medium                   | Low                  | High                          |
| Decision-making     | LLM response             | Predefined rules     | LLM selects actions           |
| Tool usage          | None                     | Fixed functions      | Dynamic tools                 |
| Private-data access | No                       | Yes                  | Yes, through tools            |
| Multi-step handling | Limited                  | Fixed steps          | Dynamic steps                 |
| Automation          | Low                      | High                 | High                          |
| Reliability         | Limited for private data | High for fixed tasks | Flexible but needs validation |

---

## 6. Suitability

For this scenario, the **AI agent** is suitable because the task requires private-data access, multiple operations, and flexible handling of the user's request.

A rule-based workflow is suitable when the steps are fixed and predictable. A plain chatbot is suitable when the user only needs general information or conversation without private-data access.

---

## 7. Conclusion

A **plain chatbot** is mainly an LLM that generates responses. A **rule-based workflow** follows predefined steps and conditions. An **AI agent** combines an LLM, tools, and a loop to dynamically select actions, observe results, and continue working toward the user's goal.


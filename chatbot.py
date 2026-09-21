import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a plain chatbot for a student expense management system.

You do NOT have access to the user's private expense records,
budget files, bank statements, or other private data.

If the user asks about their actual expenses or budget,
explain that you cannot access their private data.

Do not invent private financial information.
"""


def chatbot(user_message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    question = (
        "Analyze my expenses this month and tell me "
        "which categories are over budget."
    )

    print()
    print("=" * 72)
    print("                         PLAIN CHATBOT")
    print("=" * 72)

    print("\n[1] USER REQUEST")
    print("-" * 72)
    print(question)

    print("\n[2] PROCESS")
    print("-" * 72)
    print("LLM receives the request.")
    print("No private-data tools are available.")
    print("The chatbot cannot access expense or budget files.")

    answer = chatbot(question)

    print("\n[3] CHATBOT RESPONSE")
    print("-" * 72)
    print(answer)

    print("\n[4] CAPABILITIES")
    print("-" * 72)
    print("Private data access : NO")
    print("Tool usage          : NONE")
    print("Decision mechanism  : LLM response")
    print("Multi-step actions  : NO")

    print("\n" + "=" * 72)

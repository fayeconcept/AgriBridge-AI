import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_agriculture_ai(question: str) -> str:
    """
    Send a farmer's question to Gemini and return an agricultural response.
    """

    prompt = f"""
You are AgriBridge AI, an intelligent agricultural assistant designed
to help farmers, especially smallholder farmers in Africa.

Give practical, clear and easy-to-understand agricultural advice.

When appropriate:
- Explain possible causes of the problem.
- Give practical steps the farmer can take.
- Mention when the farmer should contact an agricultural extension officer.
- Do not pretend to be certain when there is not enough information.
- Consider African farming conditions where relevant.

Farmer's question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    question = input("Ask AgriBridge AI an agricultural question: ")
    answer = ask_agriculture_ai(question)

    print("\nAgriBridge AI:")
    print(answer)
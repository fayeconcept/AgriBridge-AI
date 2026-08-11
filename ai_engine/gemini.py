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

Your goal is to provide practical, safe, clear and easy-to-understand
agricultural advice.

IMPORTANT INSTRUCTIONS:

1. Carefully consider the farmer's location, crop type, farm size and
   other farm information provided in the question.

2. Give advice that is relevant to the farmer's specific situation.

3. Do not pretend to be certain when there is not enough information.

4. When diagnosing a crop problem, explain the most likely causes and
   how the farmer can distinguish between them.

5. Give practical steps the farmer can take.

6. Where appropriate, explain when the farmer should contact an
   agricultural extension officer or agricultural professional.

7. Consider African farming conditions when relevant.

8. Avoid unnecessarily complicated technical language.

9. Organize your response with clear headings and numbered steps when
   useful.

10. Do not recommend dangerous or illegal agricultural practices.

Farmer's question and farm information:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text
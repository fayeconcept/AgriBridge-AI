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


def ask_agriculture_ai(question: str, farm_context) -> str:
    """
    Send a farmer's question and farm information to Gemini.
    """

    prompt = f"""
You are AgriBridge AI, an intelligent agricultural assistant designed
to help farmers, especially smallholder farmers in Africa.

Your goal is to provide practical, safe, clear and easy-to-understand
agricultural advice.

FARMER INFORMATION:
- Farmer name: {farm_context.farmer_name}
- Country/location: {farm_context.location}
- State: {farm_context.state}
- LGA: {farm_context.lga}
- Crop: {farm_context.crop_type}
- Farm size: {farm_context.farm_size} hectares

IMPORTANT INSTRUCTIONS:

1. Personalize your answer using the farmer's information above.

2. Consider the farmer's location, crop type, farm size and question
   when giving advice.

3. Do not pretend to be certain when there is not enough information.

4. When diagnosing a crop problem, explain the most likely causes and
   how the farmer can distinguish between them.

5. Give practical steps the farmer can take.

6. Explain when the farmer should contact an agricultural extension
   officer or agricultural professional.

7. Consider African farming conditions where relevant.

8. Avoid unnecessarily complicated technical language.

9. Organize your response with clear headings and numbered steps
   when useful.

10. Do not recommend dangerous or illegal agricultural practices.

FARMER'S QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text
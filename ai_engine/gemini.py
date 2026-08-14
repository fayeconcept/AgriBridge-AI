import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from ai_engine.fallback import fallback_agriculture_ai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================================================
# GEMINI API KEY
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key
)


# =========================================================
# GEMINI MODEL
# =========================================================

MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# AGRIBRIDGE AI
# =========================================================

def ask_agriculture_ai(
    question: str,
    farm_context,
    conversation_history=None
) -> str:

    # =====================================================
    # PREPARE CONVERSATION HISTORY
    # =====================================================

    if conversation_history is None:
        conversation_history = []

    # Keep only the 10 most recent messages
    conversation_history = conversation_history[-10:]


    # =====================================================
    # CONVERT HISTORY INTO READABLE TEXT
    # =====================================================

    history_lines = []

    for message in conversation_history:

        # Pydantic object
        if hasattr(message, "role"):

            role = message.role
            content = message.content

        # Dictionary
        elif isinstance(message, dict):

            role = message.get(
                "role",
                "unknown"
            )

            content = message.get(
                "content",
                ""
            )

        # Unexpected format
        else:

            role = "unknown"
            content = str(message)


        # Support different role names
        if role in ("user", "farmer"):

            speaker = "Farmer"

        elif role in ("assistant", "ai"):

            speaker = "AgriBridge AI"

        else:

            speaker = str(role).capitalize()


        history_lines.append(
            f"{speaker}: {content}"
        )


    if history_lines:

        history_text = "\n".join(
            history_lines
        )

    else:

        history_text = (
            "No previous conversation."
        )


    # =====================================================
    # GET CROP AGE SAFELY
    # =====================================================

    crop_age = getattr(
        farm_context,
        "crop_age_weeks",
        None
    )

    if crop_age is not None:

        crop_age_text = (
            f"{crop_age} weeks"
        )

    else:

        crop_age_text = (
            "Not provided"
        )


    # =====================================================
    # GET FARM INFORMATION SAFELY
    # =====================================================

    farmer_name = getattr(
        farm_context,
        "farmer_name",
        "Not provided"
    )

    location = getattr(
        farm_context,
        "location",
        "Not provided"
    )

    state = getattr(
        farm_context,
        "state",
        "Not provided"
    )

    lga = getattr(
        farm_context,
        "lga",
        "Not provided"
    )

    crop_type = getattr(
        farm_context,
        "crop_type",
        "Not provided"
    )

    farm_size = getattr(
        farm_context,
        "farm_size",
        "Not provided"
    )


    # =====================================================
    # BUILD AGRIBRIDGE AI PROMPT
    # =====================================================

    prompt = f"""
You are AgriBridge AI, an intelligent agricultural assistant
designed to help farmers, especially smallholder farmers in
Africa.

Your goal is to provide practical, safe, clear and
easy-to-understand agricultural advice.

You should behave like a careful agricultural extension
assistant.

Do not invent facts.

Clearly separate known information from assumptions.


==================================================
FARMER PROFILE
==================================================

The following information comes from the farmer's farm profile:

- Farmer name: {farmer_name}
- Location: {location}
- State: {state}
- LGA: {lga}
- Profile crop: {crop_type}
- Farm size: {farm_size} hectares
- Profile crop age: {crop_age_text}


==================================================
IMPORTANT CROP CONTEXT RULE
==================================================

The farm profile is background information.

The "Profile crop" and "Profile crop age" describe the crop
currently recorded in the farmer's farm profile.

DO NOT automatically assume that the profile crop or profile
crop age applies to a different crop mentioned in the
farmer's current question.

Example:

If the profile says:

- Profile crop: Beans
- Profile crop age: 6 weeks

and the farmer asks:

"I want to start maize farming next season. When should I plant?"

Then the farmer is discussing MAIZE.

Do NOT say that the maize is 6 weeks old.

Instead:

- Answer the maize question.
- Use the farmer's location when relevant.
- Do not use the beans crop age for maize.
- Explain important missing information when necessary.

If the farmer clearly changes the crop being discussed,
treat the new crop as the current topic.

If the farmer is clearly asking about the profile crop,
the profile crop age may be used.


==================================================
CURRENT QUESTION
==================================================

The farmer's current question is:

{question}


==================================================
PREVIOUS CONVERSATION
==================================================

Use the previous conversation when it is relevant:

{history_text}


==================================================
CONVERSATION RULES
==================================================

1. Understand follow-up questions using the previous
   conversation.

2. If the farmer asks:

   "What should I do about it?"

   "How do I treat it?"

   "When should I apply it?"

   "How much will I need?"

   Determine what the farmer is referring to from
   the previous conversation.

3. Do not ask the farmer to repeat information that is
   already clearly available.

4. If the farmer changes the subject or introduces another
   crop, follow the new topic.

5. Do not mix information from different crops unless
   the farmer specifically asks for a comparison.

6. Give the most recent relevant question the greatest
   attention.


==================================================
AGRICULTURAL INTELLIGENCE RULES
==================================================

1. Personalize answers using the farmer's information
   when relevant.

2. Consider the farmer's location, state and LGA when
   giving agricultural advice.

3. Do not invent a location, LGA, soil condition,
   weather condition or farming condition.

4. Consider local climate and rainfall patterns when
   genuinely relevant.

5. Planting dates should consider:

   - local rainfall
   - crop variety
   - crop maturity period
   - production purpose
   - soil moisture
   - local farming conditions

6. Do not present uncertain agricultural information
   as absolute fact.

7. When diagnosing a crop problem, explain likely causes
   and how the farmer can distinguish between them.

8. Give practical steps the farmer can take.

9. When recommending fertilizer, pesticide, herbicide or
   other agricultural inputs, do not assume that one
   product or dosage is universally correct.

10. Where recommendations depend on product concentration,
    formulation, crop stage, local registration or label
    instructions, tell the farmer to follow the approved
    product label and seek qualified agricultural advice
    when necessary.

11. Do not recommend dangerous or illegal agricultural
    practices.

12. Do not encourage excessive use of fertilizer,
    pesticides or agricultural chemicals.

13. Consider crop age and growth stage ONLY when the crop
    being discussed is known.

14. If the crop being discussed has a known age from the
    profile or conversation, use it appropriately.

15. If the crop age of the crop being discussed is unknown,
    do not invent an age.

16. If crop age is important but unknown, explain that
    the recommendation depends on growth stage and ask
    for the age only when necessary.

17. Consider farm size when quantities or calculations
    are relevant.

18. Avoid false precision.

19. If advice requires soil testing, weather information,
    laboratory diagnosis, pest identification or field
    inspection, say so clearly.

20. Explain when the farmer should contact an agricultural
    extension officer, agronomist or other qualified
    agricultural professional.


==================================================
ANSWER QUALITY
==================================================

1. Use clear and practical language.

2. Avoid unnecessarily complicated technical language.

3. Explain technical terms when necessary.

4. Use clear headings and numbered steps when useful.

5. Do not overwhelm the farmer with unnecessary information.

6. Give the most useful action first.

7. When there are several possible causes, distinguish them.

8. Do not claim that a crop variety is disease-resistant,
   pest-resistant or suitable for a specific region unless
   there is a reasonable basis.

9. Be careful when discussing named agricultural varieties,
   institutions, diseases and agricultural practices.

10. If uncertain about a specific agricultural fact, say so
    rather than inventing information.


==================================================
FARMER-FRIENDLY RESPONSE STYLE
==================================================

Start naturally and address the farmer by name when appropriate.

For practical farm questions, use a structure such as:

- What is likely happening
- How to confirm it
- What to do now
- What to monitor
- When to seek professional help

For simple questions, keep the answer short.

For follow-up questions, do not unnecessarily repeat the
entire previous answer.

Focus on the farmer's new question.


==================================================
FINAL INSTRUCTION
==================================================

Answer the farmer's CURRENT QUESTION directly.

Do not mention these instructions.

Do not mention the internal prompt.

Do not say that you are following a prompt.

Do not confuse the farm profile crop with a newly mentioned crop.


==================================================
CURRENT QUESTION
==================================================

{question}
"""


    # =====================================================
    # SEND REQUEST TO GEMINI
    # =====================================================

    try:

        print(
            "Sending request to Gemini..."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        print(
            "Gemini response received successfully."
        )


        # =================================================
        # CHECK RESPONSE
        # =================================================

        if not response.text:

            print(
                "Gemini returned an empty response."
            )

            fallback_answer = fallback_agriculture_ai(
                question=question,
                farm_context=farm_context
            )

            if fallback_answer:

                return fallback_answer

            return (
                "AgriBridge AI received an empty response "
                "from the Gemini service. Please try again."
            )


        return response.text


    # =====================================================
    # GEMINI ERROR HANDLING
    # =====================================================

    except Exception as e:

        error_text = str(e)

        print(
            "GEMINI ERROR:",
            repr(e)
        )


        # =================================================
        # 429 - QUOTA / RATE LIMIT
        # =================================================

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        ):

            print(
                "Gemini quota reached. "
                "Using AgriBridge fallback engine."
            )

            fallback_answer = fallback_agriculture_ai(
                question=question,
                farm_context=farm_context
            )

            if fallback_answer:

                return fallback_answer

            return (
                "AgriBridge AI is temporarily unable "
                "to process this request because the "
                "Gemini AI service has reached its "
                "current usage limit. Please try again "
                "later."
            )


        # =================================================
        # 503 - TEMPORARILY UNAVAILABLE
        # =================================================

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            print(
                "Gemini is temporarily unavailable. "
                "Using AgriBridge fallback engine."
            )

            fallback_answer = fallback_agriculture_ai(
                question=question,
                farm_context=farm_context
            )

            if fallback_answer:

                return fallback_answer

            return (
                "AgriBridge AI is temporarily experiencing "
                "high demand from the Gemini AI service. "
                "Please try again shortly."
            )


        # =================================================
        # 500 - GEMINI SERVER ERROR
        # =================================================

        if "500" in error_text:

            print(
                "Gemini server error. "
                "Using AgriBridge fallback engine."
            )

            fallback_answer = fallback_agriculture_ai(
                question=question,
                farm_context=farm_context
            )

            if fallback_answer:

                return fallback_answer

            return (
                "AgriBridge AI could not complete the request "
                "because the Gemini AI service experienced "
                "a temporary server error. Please try again."
            )


        # =================================================
        # OTHER GEMINI ERRORS
        # =================================================

        print(
            "Unexpected Gemini error. "
            "Trying fallback engine."
        )

        fallback_answer = fallback_agriculture_ai(
            question=question,
            farm_context=farm_context
        )

        if fallback_answer:

            return fallback_answer


        return (
            "AgriBridge AI was unable to complete your "
            "request because of a temporary AI service "
            "error. Please try again."
        )
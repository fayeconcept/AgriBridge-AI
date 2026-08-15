import re


# =========================================================
# AGRIBRIDGE AI FALLBACK ENGINE
# =========================================================
#
# This engine is used when Gemini is unavailable,
# including quota/rate-limit situations.
#
# It provides practical answers for common agricultural
# questions without requiring an external AI service.
# =========================================================


def _get_farm_value(farm_context, name, default=None):
    """Safely get information from the farm context."""
    return getattr(
        farm_context,
        name,
        default
    )


def _get_farm_context(farm_context):
    """Collect the farmer's basic farm information."""

    return {
        "farmer_name": _get_farm_value(
            farm_context,
            "farmer_name",
            "Farmer"
        ),
        "location": _get_farm_value(
            farm_context,
            "location",
            "Not provided"
        ),
        "state": _get_farm_value(
            farm_context,
            "state",
            "Not provided"
        ),
        "lga": _get_farm_value(
            farm_context,
            "lga",
            "Not provided"
        ),
        "crop_type": _get_farm_value(
            farm_context,
            "crop_type",
            "Not provided"
        ),
        "farm_size": _get_farm_value(
            farm_context,
            "farm_size",
            None
        ),
        "crop_age_weeks": _get_farm_value(
            farm_context,
            "crop_age_weeks",
            None
        ),
    }


def _extract_number(text):
    """Find the first useful number in a question."""

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\b",
        text
    )

    if match:
        return float(match.group(1))

    return None


# =========================================================
# MAIZE SEED CALCULATOR
# =========================================================

def _maize_seed_answer(
    question,
    farm
):
    """Answer common maize seed quantity questions."""

    farm_size = farm["farm_size"]

    if farm_size is None:

        farm_size = _extract_number(question)

    if farm_size is None:

        farm_size = 1

    seed_low = farm_size * 20
    seed_high = farm_size * 25

    farmer_name = farm["farmer_name"]

    return (
        f"Hello {farmer_name},\n\n"
        f"For your **{farm_size:g} hectare(s)** of maize, "
        f"a practical planning range is approximately "
        f"**20–25 kg of certified seed per hectare**.\n\n"
        f"### Estimated seed requirement\n\n"
        f"- Farm size: **{farm_size:g} hectares**\n"
        f"- Planning rate: **20–25 kg/hectare**\n"
        f"- Estimated seed: **{seed_low:g}–{seed_high:g} kg**\n\n"
        f"If you have already bought **50 kg**, that is within "
        f"the upper end of the normal planning range for a "
        f"2-hectare farm.\n\n"
        f"### How to avoid wasting the seed\n\n"
        f"1. Follow the planting spacing recommended for your "
        f"specific maize variety.\n"
        f"2. Measure the field and divide the available seed "
        f"across the 2 hectares rather than using it all at once.\n"
        f"3. Avoid putting extra seeds in each planting hole "
        f"unless the recommended planting method calls for it.\n"
        f"4. Keep a small quantity available for gap filling "
        f"after germination.\n"
        f"5. Check the seed company's label for the recommended "
        f"plant population and seed rate.\n\n"
        f"### Important\n\n"
        f"The exact amount depends on the maize variety, seed "
        f"size, germination rate and planting method. Use the "
        f"manufacturer's recommended seed rate where it differs "
        f"from this planning estimate."
    )


# =========================================================
# MAIZE SPACING
# =========================================================

def _maize_spacing_answer(
    farm
):
    """Answer common maize spacing questions."""

    farmer_name = farm["farmer_name"]

    return (
        f"Hello {farmer_name},\n\n"
        f"For maize, a commonly used spacing arrangement is "
        f"about **75 cm between rows and 25 cm between plants** "
        f"when planting one plant per stand.\n\n"
        f"This is only a general planning guide. The recommended "
        f"spacing can vary according to the maize variety, "
        f"production system and the seed company's instructions.\n\n"
        f"Before planting, check the seed bag label for the "
        f"recommended plant population and spacing.\n\n"
        f"If you tell me the maize variety you bought, I can "
        f"help you understand the recommended spacing."
    )


# =========================================================
# FARM SIZE
# =========================================================

def _farm_size_answer(
    farm
):
    """Give a simple farm-size response."""

    farmer_name = farm["farmer_name"]
    farm_size = farm["farm_size"]

    if farm_size is None:

        return (
            f"Hello {farmer_name},\n\n"
            f"I don't yet have your farm size. Please provide "
            f"the number of hectares so I can calculate quantities "
            f"for your farm."
        )

    return (
        f"Hello {farmer_name},\n\n"
        f"Your farm profile shows a farm size of "
        f"**{farm_size:g} hectares**.\n\n"
        f"I can use this information when calculating seed, "
        f"fertilizer or other farm requirements, but the exact "
        f"rate will depend on the crop and input being discussed."
    )


# =========================================================
# CROP AGE
# =========================================================

def _crop_age_answer(
    farm
):
    """Answer when crop age is available."""

    farmer_name = farm["farmer_name"]
    crop = farm["crop_type"]
    age = farm["crop_age_weeks"]

    if age is None:

        return (
            f"Hello {farmer_name},\n\n"
            f"I don't have the age of your {crop} crop. "
            f"Please provide the crop age in weeks if your "
            f"question depends on the crop's growth stage."
        )

    return (
        f"Hello {farmer_name},\n\n"
        f"Your farm profile indicates that your {crop} crop "
        f"is approximately **{age:g} weeks old**.\n\n"
        f"Advice at this stage depends on the crop's growth "
        f"condition, variety and the specific problem you are "
        f"experiencing."
    )


# =========================================================
# GENERAL AGRICULTURAL RESPONSE
# =========================================================

def _general_answer(
    question,
    farm
):
    """Safe general response when no specific rule matches."""

    farmer_name = farm["farmer_name"]
    crop = farm["crop_type"]
    location = farm["location"]

    return (
        f"Hello {farmer_name},\n\n"
        f"I understand your question about **{crop} farming** "
        f"in **{location}**.\n\n"
        f"Gemini is temporarily unavailable, so AgriBridge AI "
        f"is using its local agricultural fallback assistant.\n\n"
        f"I can still help with basic farm planning, including "
        f"seed quantities, planting spacing, crop age and "
        f"general farm management.\n\n"
        f"For questions involving specific pesticides, "
        f"fertilizers, diseases, weather conditions or serious "
        f"crop problems, please confirm the recommendation with "
        f"a qualified agricultural extension officer or agronomist."
    )


# =========================================================
# MAIN FALLBACK FUNCTION
# =========================================================

def fallback_agriculture_ai(
    question: str,
    farm_context
) -> str:
    """
    Provide a local agricultural response when Gemini
    is unavailable.
    """

    farm = _get_farm_context(
        farm_context
    )

    question_text = (
        question
        .strip()
        .lower()
    )


    # =====================================================
    # MAIZE SEED QUESTIONS
    # =====================================================

    seed_keywords = [
        "how much seed",
        "how many kg of seed",
        "seed will i need",
        "seed do i need",
        "seed requirement",
        "seed quantity",
        "kg of seed",
        "bought 50 kg",
        "bought 50kg",
        "50 kg of seed",
        "50kg of seed",
    ]

    if (
        "maize" in question_text
        or str(farm["crop_type"]).lower() == "maize"
    ):

        if any(
            keyword in question_text
            for keyword in seed_keywords
        ):

            return _maize_seed_answer(
                question,
                farm
            )


    # =====================================================
    # MAIZE SPACING QUESTIONS
    # =====================================================

    if (
        "maize" in question_text
        or str(farm["crop_type"]).lower() == "maize"
    ):

        if (
            "spacing" in question_text
            or "distance" in question_text
            or "row" in question_text
        ):

            return _maize_spacing_answer(
                farm
            )


    # =====================================================
    # FARM SIZE QUESTIONS
    # =====================================================

    if (
        "farm size" in question_text
        or "how big is my farm" in question_text
        or "how many hectares" in question_text
    ):

        return _farm_size_answer(
            farm
        )


    # =====================================================
    # CROP AGE QUESTIONS
    # =====================================================

    if (
        "how old is my crop" in question_text
        or "crop age" in question_text
        or "how many weeks" in question_text
    ):

        return _crop_age_answer(
            farm
        )


    # =====================================================
    # GENERAL FALLBACK
    # =====================================================

    return _general_answer(
        question,
        farm
    )

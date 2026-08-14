from typing import Optional


# =========================================================
# AGRIBRIDGE AI FALLBACK ENGINE
# =========================================================
#
# This module provides basic agricultural responses when
# Gemini is temporarily unavailable.
#
# It is NOT intended to replace Gemini.
# It provides useful responses for common, calculation-based
# agricultural questions.
# =========================================================


def fallback_agriculture_ai(
    question: str,
    farm_context
) -> Optional[str]:

    """
    Provide a basic agricultural response when Gemini
    cannot process the request.

    Returns:
        str: Fallback answer
        None: If the question is outside the supported
              fallback topics.
    """

    # =====================================================
    # GET FARM INFORMATION
    # =====================================================

    farmer_name = getattr(
        farm_context,
        "farmer_name",
        "Farmer"
    )

    location = getattr(
        farm_context,
        "location",
        "your location"
    )

    state = getattr(
        farm_context,
        "state",
        ""
    )

    lga = getattr(
        farm_context,
        "lga",
        ""
    )

    crop_type = getattr(
        farm_context,
        "crop_type",
        ""
    )

    farm_size = getattr(
        farm_context,
        "farm_size",
        None
    )

    crop_age = getattr(
        farm_context,
        "crop_age_weeks",
        None
    )


    # =====================================================
    # NORMALIZE QUESTION
    # =====================================================

    q = question.lower().strip()


    # =====================================================
    # DETECT MAIZE
    # =====================================================

    maize_question = (
        "maize" in q
        or "corn" in q
    )


    # =====================================================
    # SEED REQUIREMENT
    # =====================================================

    seed_keywords = [
        "seed",
        "seeds",
        "how much seed",
        "seed quantity",
        "seed rate",
        "kg of seed",
        "kilogram of seed"
    ]

    asks_seed = any(
        keyword in q
        for keyword in seed_keywords
    )


    if maize_question and asks_seed:

        if farm_size is not None:

            try:
                hectares = float(farm_size)

                if hectares > 0:

                    low_rate = 20
                    high_rate = 25

                    low_quantity = hectares * low_rate
                    high_quantity = hectares * high_rate

                    return (
                        f"Hello {farmer_name},\n\n"
                        f"For maize farming on your "
                        f"{hectares:g}-hectare farm in "
                        f"{location}, a commonly used "
                        f"planning range is approximately "
                        f"{low_rate}–{high_rate} kg of "
                        f"certified seed per hectare.\n\n"
                        f"### Estimated seed requirement\n\n"
                        f"- Farm size: {hectares:g} hectares\n"
                        f"- Planning rate: {low_rate}–{high_rate} kg/hectare\n"
                        f"- Estimated seed: "
                        f"**{low_quantity:g}–{high_quantity:g} kg**\n\n"
                        f"So, for your farm, plan for approximately "
                        f"**{low_quantity:g}–{high_quantity:g} kg "
                        f"of maize seed**.\n\n"
                        f"The exact seed requirement can vary "
                        f"depending on variety, planting spacing, "
                        f"seed size and the recommended plant "
                        f"population. Check the seed company's "
                        f"recommended planting rate before buying.\n\n"
                        f"Buy certified seed from a reliable "
                        f"agricultural seed supplier."
                    )

            except (TypeError, ValueError):
                pass


    # =====================================================
    # GENERAL MAIZE PLANTING
    # =====================================================

    planting_keywords = [
        "when should i plant",
        "when can i plant",
        "when to plant",
        "planting time",
        "plant maize",
        "planting maize"
    ]

    asks_planting = any(
        keyword in q
        for keyword in planting_keywords
    )


    if maize_question and asks_planting:

        return (
            f"Hello {farmer_name},\n\n"
            f"For maize farming in {location}, "
            f"planting should generally be timed with "
            f"the establishment of reliable rainfall for "
            f"rainfed production.\n\n"
            f"### Before planting\n\n"
            f"1. Prepare the land before the main rains "
            f"become established.\n"
            f"2. Wait for consistent rainfall and adequate "
            f"soil moisture rather than relying on one "
            f"isolated shower.\n"
            f"3. Choose a maize variety appropriate for "
            f"your local growing conditions and intended "
            f"harvest period.\n"
            f"4. Have certified seed and fertilizer ready "
            f"before planting.\n\n"
            f"The exact planting window can vary by season, "
            f"rainfall pattern, variety and location. For "
            f"your farm in {location}, a local agricultural "
            f"extension officer can provide the most "
            f"accurate seasonal recommendation."
        )


    # =====================================================
    # MAIZE SPACING
    # =====================================================

    spacing_keywords = [
        "spacing",
        "plant spacing",
        "plant distance",
        "row spacing",
        "how far apart"
    ]

    asks_spacing = any(
        keyword in q
        for keyword in spacing_keywords
    )


    if maize_question and asks_spacing:

        return (
            f"Hello {farmer_name},\n\n"
            f"For maize, spacing is important because it "
            f"affects plant population and yield.\n\n"
            f"A commonly used starting point is around "
            f"**75 cm between rows and 25 cm between plants** "
            f"with one healthy plant per stand.\n\n"
            f"However, the recommended spacing can differ "
            f"by variety, target plant population, soil "
            f"fertility and production system.\n\n"
            f"Check the seed manufacturer's recommendation "
            f"for the particular variety you are planting."
        )


    # =====================================================
    # FARM SIZE
    # =====================================================

    farm_size_keywords = [
        "farm size",
        "hectares",
        "hectare",
        "how big is my farm"
    ]

    asks_farm_size = any(
        keyword in q
        for keyword in farm_size_keywords
    )


    if asks_farm_size and farm_size is not None:

        try:

            hectares = float(farm_size)

            if hectares > 0:

                return (
                    f"Your farm profile currently shows "
                    f"**{hectares:g} hectares**.\n\n"
                    f"This farm size can be used to estimate "
                    f"seed, fertilizer and other input "
                    f"requirements, but the exact quantity "
                    f"depends on the crop and recommended "
                    f"application rate."
                )

        except (TypeError, ValueError):
            pass


    # =====================================================
    # CROP AGE
    # =====================================================

    age_keywords = [
        "crop age",
        "how old",
        "how many weeks",
        "crop is"
    ]

    asks_crop_age = any(
        keyword in q
        for keyword in age_keywords
    )


    if asks_crop_age and crop_age is not None:

        return (
            f"The current farm profile shows the crop age "
            f"as approximately **{crop_age} weeks**.\n\n"
            f"Crop-stage recommendations should also "
            f"consider the specific crop, variety and "
            f"actual field condition."
        )


    # =====================================================
    # GENERAL FALLBACK
    # =====================================================

    return (
        f"Hello {farmer_name},\n\n"
        f"I understand your question about farming "
        f"in {location}.\n\n"
        f"Gemini is temporarily unavailable, so I cannot "
        f"provide the full AgriBridge AI analysis right now.\n\n"
        f"Your farm profile is still available:\n\n"
        f"- Location: {location}\n"
        f"- State: {state}\n"
        f"- LGA: {lga}\n"
        f"- Profile crop: {crop_type}\n"
        f"- Farm size: {farm_size} hectares\n\n"
        f"Please try the question again when the AI service "
        f"is available. For important farm decisions, "
        f"confirm recommendations with a qualified "
        f"agricultural extension officer."
    )
"""Rule-based risk scoring.

Matches a user's stated condition and personal triggers against reported
environmental conditions for a destination or occasion. No external API
call yet — air_quality_level and pollen_level are supplied by the form
(travel/routes.py). Swapping in a live AQI/weather API later just means
computing these two values automatically instead of asking the user.
"""

CONDITION_KEYWORDS = {
    "asthma": ["dust", "smoke", "pollen", "cold air", "exercise"],
    "copd": ["smoke", "dust", "pollution", "cold air"],
    "pollen allergy": ["pollen", "grass", "flowers"],
    "hay fever": ["pollen", "grass"],
    "eczema": ["heat", "sweat", "dust", "wool"],
    "migraine": ["bright light", "strong smell", "heat"],
}


def assess_risk(user, air_quality_level, pollen_level):
    """Returns (risk_level: 'Low'|'Moderate'|'High', reasons: list[str])."""

    reasons = []
    score = 0

    disease = (user.disease or "").lower()
    user_triggers = [t.strip().lower() for t in (user.trigger or "").split(",") if t.strip()]

    if air_quality_level == "High":
        score += 2
        reasons.append("Air quality is reported as high pollution.")
    elif air_quality_level == "Moderate":
        score += 1

    if pollen_level == "High":
        score += 2
        reasons.append("Pollen levels are reported as high.")
    elif pollen_level == "Moderate":
        score += 1

    known_keywords = []
    for condition, keywords in CONDITION_KEYWORDS.items():
        if condition in disease:
            known_keywords.extend(keywords)

    if "pollen" in known_keywords and pollen_level in ("Moderate", "High"):
        score += 1
        reasons.append(f"Pollen exposure is a known concern for {user.disease}.")

    if any(k in known_keywords for k in ["smoke", "dust", "pollution"]) and air_quality_level in ("Moderate", "High"):
        score += 1
        reasons.append(f"Poor air quality is a known concern for {user.disease}.")

    for trigger in user_triggers:
        if "pollen" in trigger and pollen_level in ("Moderate", "High"):
            score += 1
            reasons.append(f"You've noted '{trigger}' as a personal trigger, and pollen is elevated.")
        if any(w in trigger for w in ["dust", "smoke", "air", "pollution"]) and air_quality_level in ("Moderate", "High"):
            score += 1
            reasons.append(f"You've noted '{trigger}' as a personal trigger, and air quality is degraded.")

    if score >= 4:
        risk_level = "High"
    elif score >= 2:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    if not reasons:
        reasons.append("Nothing in the reported conditions matched your known triggers.")

    return risk_level, reasons

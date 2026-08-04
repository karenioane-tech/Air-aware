"""Turns a risk level into concrete, actionable advice for the patient."""

BASE_TIPS = {
    "High": [
        "Carry your rescue medication with you at all times.",
        "Consider rescheduling or shortening outdoor exposure if possible.",
        "Let someone know your plans in case you need help.",
    ],
    "Moderate": [
        "Keep your medication accessible.",
        "Limit prolonged outdoor activity, especially during peak hours.",
        "Watch how you're feeling and log symptoms if anything changes.",
    ],
    "Low": [
        "Conditions look manageable — standard precautions should be enough.",
        "Still worth carrying medication if you use a rescue inhaler or similar.",
    ],
}


def build_recommendations(risk_level, user):
    tips = list(BASE_TIPS.get(risk_level, BASE_TIPS["Low"]))

    if user.medication:
        tips.insert(0, f"Bring your {user.medication}.")

    return tips

def classify_post(text: str):
    text_lower = text.lower()
    hazard = "Other"
    urgency = "Low"

    if any(word in text_lower for word in ["cyclone", "hurricane", "storm"]):
        hazard = "Cyclone"
    elif any(word in text_lower for word in ["flood", "rain", "inundation"]):
        hazard = "Flood"
    elif any(word in text_lower for word in ["earthquake", "tremor"]):
        hazard = "Earthquake"

    if any(word in text_lower for word in ["urgent", "danger", "emergency", "very dangerous", "alert"]):
        urgency = "High"
    elif any(word in text_lower for word in ["warning", "caution"]):
        urgency = "Medium"

    return hazard, urgency

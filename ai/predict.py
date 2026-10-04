import re


# ==========================================================
# CATEGORY KEYWORDS
# ==========================================================

CATEGORY_KEYWORDS = {

    "Water / Infrastructure": [
        "water",
        "pipe",
        "leak",
        "leakage",
        "flood",
        "drainage",
        "tap",
        "plumbing",
        "sewage",
        "building",
        "road",
        "ceiling",
        "wall",
        "infrastructure"
    ],

    "Electricity": [
        "electricity",
        "power",
        "current",
        "electric",
        "wire",
        "shock",
        "transformer",
        "light",
        "fan",
        "voltage",
        "short circuit"
    ],

    "Internet / Technology": [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "connection",
        "connectivity",
        "disconnect",
        "disconnected",
        "disconnecting",
        "router",
        "bandwidth",
        "online",
        "server",
        "website",
        "portal",
        "system",
        "login",
        "computer",
        "software",
        "technical"
    ],

    "Hostel": [
        "hostel",
        "room",
        "warden",
        "bed",
        "mess",
        "food",
        "canteen",
        "dormitory"
    ],

    "Academic": [
        "exam",
        "marks",
        "faculty",
        "teacher",
        "class",
        "attendance",
        "assignment",
        "lab",
        "subject",
        "lecture",
        "syllabus",
        "course",
        "academic"
    ],

    "Transport": [
        "bus",
        "transport",
        "driver",
        "vehicle",
        "route",
        "college bus"
    ],

    "Security": [
        "security",
        "theft",
        "stolen",
        "fight",
        "harassment",
        "unsafe",
        "camera",
        "cctv",
        "intruder",
        "threat",
        "violence"
    ],

    "Cleanliness": [
        "garbage",
        "waste",
        "dirty",
        "clean",
        "dustbin",
        "sanitation",
        "smell",
        "hygiene"
    ]
}


# ==========================================================
# PRIORITY KEYWORDS
# ==========================================================

SAFETY_KEYWORDS = [
    "danger",
    "dangerous",
    "unsafe",
    "accident",
    "injury",
    "injured",
    "fire",
    "shock",
    "electric shock",
    "flood",
    "major leak",
    "emergency",
    "life risk",
    "threat",
    "violence"
]


URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "immediate",
    "as soon as possible",
    "emergency",
    "critical",
    "serious",
    "quickly",
    "cannot wait",
    "right away"
]


IMPACT_KEYWORDS = [
    "students",
    "people",
    "everyone",
    "entire",
    "whole",
    "many",
    "multiple",
    "several",
    "campus",
    "hostel",
    "all students"
]


# ==========================================================
# HIGH IMPACT / SERVICE INTERRUPTION
# ==========================================================

HIGH_IMPACT_KEYWORDS = [
    "exam failure",
    "exam failed",
    "exam session",
    "online exam",
    "online examination",
    "certification exam",
    "losing attempts",
    "lost attempts",
    "attempts are failing",
    "attempt failed",
    "unable to attend",
    "unable to access",
    "cannot access",
    "system failure",
    "service outage",
    "network outage",
    "internet outage",
    "wifi outage",
    "frequently disconnect",
    "frequently disconnects",
    "keeps disconnecting",
    "repeatedly disconnects",
    "connection keeps dropping",
    "connection drops",
    "work is blocked",
    "classes are affected",
    "exam is affected",
    "exams are affected"
]


# ==========================================================
# REPEATED / LONG-DURATION ISSUE
# ==========================================================

DURATION_KEYWORDS = [
    "for days",
    "for a day",
    "for two days",
    "for three days",
    "for several days",
    "for weeks",
    "for a week",
    "since yesterday",
    "since last week",
    "past few days",
    "past few weeks",
    "continuing",
    "ongoing",
    "repeatedly",
    "frequently"
]


# ==========================================================
# CATEGORY DETECTION
# ==========================================================

def detect_category(text):

    text = text.lower()

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[category] = score


    # ------------------------------------------------------
    # Special priority for technology/network complaints
    # ------------------------------------------------------

    technology_keywords = [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "connectivity",
        "router",
        "bandwidth",
        "disconnect",
        "disconnected",
        "disconnecting"
    ]

    technology_score = sum(
        1 for keyword in technology_keywords
        if keyword in text
    )

    if technology_score > 0:

        scores["Internet / Technology"] += (
            technology_score * 2
        )


    best_category = max(
        scores,
        key=scores.get
    )


    # No keyword matched
    if scores[best_category] == 0:

        return "General"


    return best_category


# ==========================================================
# PRIORITY ANALYSIS
# ==========================================================

def calculate_priority(text):

    text = text.lower()

    score = 0

    reasons = []


    # ------------------------------------------------------
    # SAFETY
    # ------------------------------------------------------

    safety_matches = [
        keyword
        for keyword in SAFETY_KEYWORDS
        if keyword in text
    ]

    if safety_matches:

        score += 30

        reasons.append(
            "Potential safety risk detected"
        )


    # ------------------------------------------------------
    # URGENCY
    # ------------------------------------------------------

    urgency_matches = [
        keyword
        for keyword in URGENCY_KEYWORDS
        if keyword in text
    ]

    if urgency_matches:

        score += 20

        reasons.append(
            "Urgency indicators detected"
        )


    # ------------------------------------------------------
    # MULTIPLE PEOPLE / LARGE IMPACT
    # ------------------------------------------------------

    impact_matches = [
        keyword
        for keyword in IMPACT_KEYWORDS
        if keyword in text
    ]

    if impact_matches:

        score += 20

        reasons.append(
            "Multiple people or a large area may be affected"
        )


    # ------------------------------------------------------
    # HIGH-IMPACT SERVICE INTERRUPTION
    # ------------------------------------------------------

    high_impact_matches = [
        keyword
        for keyword in HIGH_IMPACT_KEYWORDS
        if keyword in text
    ]

    if high_impact_matches:

        score += 30

        reasons.append(
            "Important service or academic activity is being disrupted"
        )


    # ------------------------------------------------------
    # LONG / REPEATED ISSUE
    # ------------------------------------------------------

    duration_matches = [
        keyword
        for keyword in DURATION_KEYWORDS
        if keyword in text
    ]

    if duration_matches:

        score += 15

        reasons.append(
            "Issue appears to be repeated or ongoing"
        )


    # ------------------------------------------------------
    # DETAILED COMPLAINT
    # ------------------------------------------------------

    if len(text.split()) > 25:

        score += 10

        reasons.append(
            "Detailed complaint indicates a significant issue"
        )


    # ------------------------------------------------------
    # INFRASTRUCTURE SEVERITY
    # ------------------------------------------------------

    infrastructure_words = [
        "flood",
        "fire",
        "leak",
        "broken",
        "damage",
        "collapse"
    ]

    if any(
        word in text
        for word in infrastructure_words
    ):

        score += 20

        reasons.append(
            "Infrastructure or physical damage detected"
        )


    # ------------------------------------------------------
    # NETWORK / TECHNOLOGY FAILURE
    # ------------------------------------------------------

    technology_failure_words = [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "disconnect",
        "disconnected",
        "disconnecting",
        "connection",
        "connectivity",
        "server",
        "system failure"
    ]

    technology_failure_count = sum(
        1
        for word in technology_failure_words
        if word in text
    )

    if technology_failure_count >= 2:

        score += 15

        reasons.append(
            "Technology or network service disruption detected"
        )


    # ------------------------------------------------------
    # CAP SCORE
    # ------------------------------------------------------

    score = min(score, 100)


    # ------------------------------------------------------
    # PRIORITY LEVEL
    # ------------------------------------------------------

    if score >= 80:

        priority = "CRITICAL"

    elif score >= 60:

        priority = "HIGH"

    elif score >= 40:

        priority = "MEDIUM"

    else:

        priority = "LOW"


    # ------------------------------------------------------
    # DEFAULT REASON
    # ------------------------------------------------------

    if not reasons:

        reasons.append(
            "No major urgency or safety indicators detected"
        )


    return priority, score, reasons


# ==========================================================
# DEPARTMENT RECOMMENDATION
# ==========================================================

DEPARTMENT_MAP = {

    "Water / Infrastructure":
        "Maintenance",

    "Electricity":
        "Electrical Maintenance",

    "Internet / Technology":
        "IT / Network",

    "Hostel":
        "Hostel Administration",

    "Academic":
        "Academic Department",

    "Transport":
        "Transport Department",

    "Security":
        "Security Department",

    "Cleanliness":
        "Sanitation Department",

    "General":
        "Administration"
}


def recommend_department(category):

    return DEPARTMENT_MAP.get(
        category,
        "Administration"
    )


# ==========================================================
# COMPLETE ANALYSIS
# ==========================================================

def analyze_complaint(text):

    category = detect_category(text)

    priority, score, reasons = calculate_priority(text)

    department = recommend_department(category)

    return {
        "category": category,
        "priority": priority,
        "score": score,
        "department": department,
        "reasons": reasons
    }
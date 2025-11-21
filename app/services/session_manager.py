import uuid

# In-memory session store (simple MVP)
SESSIONS = {}


def create_session(resume_json, jd_json):
    """
    Creates a new interview session with resume + job description parsed data.
    Stores full interview state in memory.
    """
    session_id = str(uuid.uuid4())

    SESSIONS[session_id] = {
        "session_id": session_id,

        # Parsed input data
        "resume": resume_json,
        "jd": jd_json,

        # Question flow
        "questions": [],
        "current": 0,                 # index of main question

        # Follow-up question flow
        "followup_pending": None,     # store current follow-up question text
        "followup_count": 0,          # how many follow-ups asked for this main question (max 3)

        # Answers + evaluations
        "answers": [],                # list of user answers + evaluations

        # Final output
        "final_plan": None            # improvement plan summary
    }

    return session_id


def get_session(session_id: str):
    """
    Retrieve a session safely.
    """
    return SESSIONS.get(session_id)


def update_session(session_id: str, data: dict):
    """
    Update session keys partially.
    """
    if session_id in SESSIONS:
        SESSIONS[session_id].update(data)
        return True
    return False

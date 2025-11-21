# app/routes/answer.py

from fastapi import APIRouter, Form
from app.services.session_manager import SESSIONS
from app.services.evaluator_service import evaluate_answer
from app.services.followup_service import generate_followup

router = APIRouter()

# If combined score < threshold → generate follow-up
FOLLOWUP_SCORE_THRESHOLD = 0.55    # (semantic+bert)/2 cut-off


@router.post("/submit-answer")
async def submit_answer(
    session_id: str = Form(...),
    transcript: str = Form(...)
):
    session = SESSIONS.get(session_id)
    if not session:
        return {"error": "Invalid session_id"}

    # -----------------------------------------------------
    # 1️⃣ DETERMINE IF THIS IS A FOLLOW-UP ANSWER
    # -----------------------------------------------------
    is_followup = False

    if session.get("followup_pending"):
        is_followup = True
        question_text = session["followup_pending"]
        question_id = f"followup_{session['followup_count']}"
        question_obj = None  # follow-ups have no expected_points
    else:
        idx = session["current"]
        if idx >= len(session["questions"]):
            return {"type": "finished", "message": "Interview complete."}

        question_obj = session["questions"][idx]
        question_text = question_obj["text"]
        question_id = question_obj["id"]

    # -----------------------------------------------------
    # 2️⃣ HYBRID EVALUATION (semantic + BERTScore + LLM)
    # -----------------------------------------------------
    evaluation = await evaluate_answer(
        question_text=question_text,
        user_answer=transcript
    )

    combined_score = evaluation.get("combined_score", 0.0)
    missing_keywords = evaluation.get("missing_keywords", []) or []

    # -----------------------------------------------------
    # 3️⃣ STORE THE ANSWER WITH EVALUATION
    # -----------------------------------------------------
    session["answers"].append({
        "question_id": question_id,
        "is_followup": is_followup,
        "question_text": question_text,
        "transcript": transcript,
        "evaluation": evaluation
    })

    # -----------------------------------------------------
    # 4️⃣ IF THIS WAS A FOLLOW-UP ANSWER
    # -----------------------------------------------------
    if is_followup:
        # If the answer is still weak → generate another follow-up (max 3)
        if combined_score < FOLLOWUP_SCORE_THRESHOLD and session["followup_count"] < 3:
            main_q_text = session["questions"][session["current"]]["text"]
            new_followup = (await generate_followup(main_q_text, transcript)).get("followup")

            if new_followup:
                session["followup_pending"] = new_followup
                session["followup_count"] += 1

                return {
                    "type": "followup",
                    "evaluation": evaluation,
                    "followup": new_followup,
                    "followup_count": session["followup_count"]
                }

        # else → clear followup & move to next main question
        session["followup_pending"] = None
        session["followup_count"] = 0
        session["current"] += 1

        if session["current"] >= len(session["questions"]):
            return {"type": "finished", "evaluation": evaluation}

        return {
            "type": "next_main_question",
            "evaluation": evaluation,
            "next_question": session["questions"][session["current"]]
        }

    # -----------------------------------------------------
    # 5️⃣ MAIN QUESTION ANSWER — DECIDE IF FOLLOW-UP NEEDED
    # -----------------------------------------------------
    need_followup = False

    # Condition 1 — weak score
    if combined_score < FOLLOWUP_SCORE_THRESHOLD:
        need_followup = True

    # Condition 2 — lots of missing keywords
    if len(missing_keywords) >= 2 and session["followup_count"] < 3:
        need_followup = True

    # If follow-up needed
    if need_followup and session["followup_count"] < 3:
        new_followup = (await generate_followup(question_text, transcript)).get("followup")
        if new_followup:
            session["followup_pending"] = new_followup
            session["followup_count"] += 1
            return {
                "type": "followup",
                "evaluation": evaluation,
                "followup": new_followup,
                "followup_count": session["followup_count"]
            }

    # -----------------------------------------------------
    # 6️⃣ NO FOLLOW-UP → MOVE TO NEXT MAIN QUESTION
    # -----------------------------------------------------
    session["followup_pending"] = None
    session["followup_count"] = 0
    session["current"] += 1

    if session["current"] >= len(session["questions"]):
        return {"type": "finished", "evaluation": evaluation}

    return {
        "type": "next_main_question",
        "evaluation": evaluation,
        "next_question": session["questions"][session["current"]]
    }

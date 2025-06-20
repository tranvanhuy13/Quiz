import datetime

from flask import Blueprint, request, jsonify

from app.database.database import MockDatabase
from utils.quiz import Utils

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/v1/quiz")

@quiz_bp.route("/get-questions", methods=["GET"])
def get_questions():
    quiz = Utils.prepare_quiz(5)
    MockDatabase.save_quiz(quiz)
    questions = quiz.get("data").get("questions")
    res_question = Utils.remove_answer(questions)
    return {
        "quiz_id": quiz.get("quiz_id"),
        "questions": res_question
    }

@quiz_bp.route("/validate-question", methods=["POST"])
def validate_question(quiz_id):
    data = request.get_json()

    quiz_id = data.get("quiz_id")
    question_id = data.get("question_id")
    selected_option = data.get("selected_option")

    if not all([quiz_id, question_id is not None, selected_option is not None]):
        return jsonify({"error": "Missing required fields"}), 400

    db = MockDatabase()
    quiz = db.get_quiz(quiz_id)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    question = next((q for q in quiz["questions"] if q["id"] == question_id), None)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    is_correct = question["answer"] == selected_option

    # Save the answer
    quiz.setdefault("answers", []).append({
        "question_id": question_id,
        "selected_option": selected_option,
        "correct": is_correct
    })

    db.save_quiz(quiz)

    return jsonify({
        "question_id": question_id,
        "correct": is_correct,
        "message": "Correct!" if is_correct else "Incorrect!"
    })

@quiz_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    quiz_id = data.get("quiz_id")
    if not quiz_id:
        return jsonify({"error": "Quiz ID is required"}), 400

    db = MockDatabase()
    quiz = db.get_quiz(quiz_id)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    total_questions = len(quiz["questions"])
    correct_answers = sum(1 for a in quiz.get("answers", []) if a.get("correct") is True)

    result = {
        "quiz_id": quiz_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percent": round((correct_answers / total_questions) * 100, 2),
        "passed": correct_answers >= total_questions * 0.6,  # 60% passing rule
        "review": [
            {
                "question_id": q["id"],
                "question": q["question"],
                "correct_option": q["options"][q["answer"]],
                "user_selected": next((a["selected_option"] for a in quiz["answers"] if a["question_id"] == q["id"]), None),
                "is_correct": next((a["correct"] for a in quiz["answers"] if a["question_id"] == q["id"]), False)
            } for q in quiz["questions"]
        ]
    }

    return jsonify(result)

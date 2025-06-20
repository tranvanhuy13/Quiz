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
    json_data = request.get_json()

    quiz_id = json_data.get("quiz_id")
    answers = json_data.get("options")

    if not quiz_id or not isinstance(answers, list):
        return jsonify({"error": "Invalid input"}), 400
    db = MockDatabase()
    session = db.get_quiz(quiz_id)
    if not session:
        return jsonify({"error": "Invalid quiz ID"}), 404
    result = []
    correct_count = 0
    for item in answers:
        question_id = item.get("question_id")
        selected_option = item.get("selected_option")

        if question_id is None or selected_option is None:
            continue

        # Find the question in this session
        question = next((q for q in session["questions"] if q["id"] == question_id), None)

        if not question:
            continue

        is_correct = question["answer"] == selected_option
        result.append({
            "question_id": question_id,
            "selected": selected_option,
            "correct": is_correct
        })

        session["answers"].append({
            "question_id": question_id,
            "selected": selected_option,
            "correct": is_correct
        })

        if is_correct:
            correct_count += 1

        return jsonify({
            "quiz_id": quiz_id,
            "total": len(result),
            "correct": correct_count,
            "incorrect": len(result) - correct_count,
            "time": datetime.datetime.utcnow()- session["start_time"],
            "details": result
        })



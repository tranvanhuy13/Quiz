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

@quiz_bp.route("/<quiz_id>/validate-question", methods=["POST"])
def validate_question(quiz_id):
    data = request.get_json()

    selected_option = data.get("selected_option")

    if selected_option is None:
        return jsonify({}),400

    quiz = MockDatabase.get_quiz(quiz_id)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    current_question = quiz.get("data").get("current_question")
    answers = quiz.get("data").get("questions")[current_question].get("answer")

    correct_answer = selected_option == answers
    MockDatabase.update_current_question(quiz_id)
    data ={
        "correct_answer": answers,
        "status": correct_answer,
        "feedback": Utils.get_feedback(correct_answer)
    }
    size = MockDatabase.get_size(quiz_id)
    if current_question == size - 1:
        MockDatabase.update_end_time(quiz_id)
    MockDatabase.append_session(quiz_id,data)
    return jsonify(data)

@quiz_bp.route("/<quiz_id>/result", methods=["GET"])
def result(quiz_id):
    quiz = MockDatabase.get_quiz(quiz_id)
    data = quiz.get("data")
    answers = data.get("answers")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    size = MockDatabase.get_size(quiz_id)
    correct_answer = 0
    for answer in answers:
        if answer.get("status"):
            correct_answer += 1
    return jsonify({
        "time":(end_time.timestamp() - start_time.timestamp()) // 1000,
        "correct_answer": correct_answer,
        "incorrect_answers": size - correct_answer,
    })

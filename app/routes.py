from flask import Blueprint

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



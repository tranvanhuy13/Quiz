import random
from datetime import datetime
from uuid import uuid4

from app.data import QUESTIONS


class Utils:
    @classmethod
    def prepare_quiz(cls, ques_number: int):
        # quiz_id = uuid4()
        quiz_id = 1
        generated_questions = cls.get_random_questions(ques_number)
        return {
            "quiz_id": quiz_id,
            "data": {
                "start_time": datetime.utcnow(),
                "end_time": None,
                "answers": [],
                "current_question": 0,
                "questions": generated_questions
            }
        }

    @staticmethod
    def remove_answer(questions):
        return [
            {
                "question": question.get("question"),
                "options": question.get("options")
            } for question in questions
        ]



    @staticmethod
    def get_random_questions(n):
        return random.sample(QUESTIONS, min(n, len(QUESTIONS)))

    @staticmethod
    def get_feedback(correct):
        return "Correct" if correct else "Incorrect"

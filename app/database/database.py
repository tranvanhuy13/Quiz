import datetime


class MockDatabase:
    _instance = None

    def __init__(self):
        self.quiz_datas = {}
    @classmethod
    def get_size(cls,quiz_id):
        return len(cls.get_instance().quiz_datas.get(quiz_id).get("data").get("questions"))

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def save_quiz(cls, quiz):
        instance = cls.get_instance()
        print("saving quiz", quiz)
        instance.quiz_datas[str(quiz.get("quiz_id"))] = quiz

    @classmethod
    def get_quiz(cls, quiz_id):
        instance = cls.get_instance()
        return instance.quiz_datas.get(quiz_id)

    @classmethod
    def update_current_question(cls,quid_id):
        quiz_session = cls.get_quiz(quid_id)
        quiz_session["data"]["current_question"] += 1
        cls.save_quiz(quiz_session)

    @classmethod
    def append_session(cls,quiz_id,data):
        quiz_session = cls.get_quiz(quiz_id)
        quiz_session["data"]["answers"].append(data)
        cls.save_quiz(quiz_session)
    @classmethod
    def update_end_time(cls,quid_id):
        quiz_session = cls.get_quiz(quid_id)
        quiz_session["data"]["end_time"] = datetime.datetime.now()
        cls.save_quiz(quiz_session)

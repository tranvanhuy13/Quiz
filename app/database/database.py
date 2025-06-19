class MockDatabase:
    _instance = None

    def __init__(self):
        self.quiz_datas = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def save_quiz(cls, quiz):
        instance = cls.get_instance()
        print("saving quiz", quiz)
        instance.quiz_datas[quiz.get("quiz_id")] = quiz

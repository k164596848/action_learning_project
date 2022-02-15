from core.activity import Activity


class Distribution:
    activity: Activity
    gender: str
    age: int
    height: float

    def __init__(
        self, activity: Activity, gender: str = "男", age: int = 65, height: float = 165
    ):
        self.activity = Activity(activity)
        self.gender = gender
        self.age = age
        self.height = height

from operator import gt, lt
from typing import Callable

import pandas as pd


class CoachData:
    """Coach's data that coach is a target when compare method is called."""

    path = "data/coach.csv"

    @classmethod
    def _read(cls) -> pd.DataFrame:
        return pd.read_csv(cls.path).astype("string")

    @classmethod
    def get_uuids(cls) -> list:
        df = cls._read()
        return list(df["uuid"].values)

    @classmethod
    def get(cls):
        df = cls._read()
        return df.to_dict("records")

    @classmethod
    def add(cls, data: dict) -> bool:
        uuid = data["uuid"]
        df = cls._read()
        if uuid in df["uuid"].values:
            return False
        df = df.append(data, ignore_index=True)
        cls._save(df)
        return True

    # TODO: Change, Remove

    @classmethod
    def _save(cls, df: pd.DataFrame):
        df.to_csv(cls.path, index=False)


class ActionLevel:
    """ActionLevel is a class for evaluating level current action to target activity."""

    _data:list

    level_table = {"不好": 20, "稍差": 40, "普通": 60, "尚好": 75, "很好": 99}

    def __init__(self, action_name, gender="男", age=65, data=0, reverse=False):
        """
        gender: 男, 女
        """
        self.action_name = action_name
        self.gender = gender
        self.age = age
        self.data = data
        self.reverse = reverse
        self._init_data()

    @property
    def compare(self) -> Callable:
        """Get comparsion operator"""
        if self.reverse:
            return lt
        return gt

    def _init_data(self):
        """Load dataset and store to self._data"""
        df = pd.read_csv(
            "data/" + self.action_name + "-" + self.gender + ".csv", header=0
        )
        
        self._data = df

    def _get_age_column(self) -> str:
        for low_bound in list(map(int, reversed(self._data.columns.values[1:]))):
            if self.age >= low_bound:
                return str(low_bound)
        # raise ValueError(f"age {self.age} maybe a wrong value")
        return str(65)

    def _get_percentile_rank(self, col_name) -> int:
        for index, c in enumerate(reversed(self._data[col_name].values)):
            if self.compare(self.data, c):
                pr = (len(self._data[col_name].values) - index) * 5
                assert 0 <= int(pr) <= 99
                return pr
        return 0

    def get_percentile_rank(self) -> int:
        """PR Value

        Returns:
            int: 0-99
        """
        # Get col of age
        age_col = self._get_age_column()
        # Get pr
        pr = self._get_percentile_rank(age_col)
        return pr

    def level(self):#here is tester Pr value in  the csv file 
        """Get level name reference to `level_table`

        Raises:
            ValueError: When pr is out of 0-99

        Returns:
            str: Level name
        """
        pr = self.get_percentile_rank()
        print ("the pr vlaue is = ",pr ,"||from ActionLevel calss level() ")
        for level_name, upbound in self.level_table.items():
            if upbound >= pr:
                return level_name
        raise ValueError(f"PR: {pr} Out of range 0-99")

    def get_info(self) -> dict:
        """Get full information

        Returns:
            dict: all information
        """
        return {
            "動作": self.action_name,
            "年齡": self.age,
            "性別": self.gender,
            "程度": self.level(),
        }

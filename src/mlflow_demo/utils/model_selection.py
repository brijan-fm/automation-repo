import numpy as np
import pandas as pd

from sklearn.model_selection import BaseCrossValidator

class TimeBasedSplit(BaseCrossValidator):
    def __init__(self, n_splits:int, test_size:int, step_size:int, time_idx_name:str="year_week"):
        """Initilize the time based split for cross validation

        Parameters
        ----------
        n_splits : int
            Number of cross-validation splits
        test_size : int
            no. of time units in the test sets
        step_size : int
            number of time units to move the test window for next split
        time_idx_name : str, optional
            name of the time index level in the dataframe, by default "year_week"
        """
        self.n_splits = n_splits
        self.test_size = test_size
        self.step_size = step_size
        self.time_idx_name = time_idx_name

    def split(self, X, y = None, groups = None):
        if not isinstance(X, pd.DataFrame):
            raise ValueError("X must be a pandas DataFrame")
        
        if self.time_idx_name not in X.index.names:
            raise ValueError(f"X must contain {self.time_idx_name} in its index")
        
        time_idx = X.index.get_level_values(self.time_idx_name)
        time_range = np.sort(time_idx.unique())
        min_required_size = self.test_size + (self.n_splits - 1) * self.step_size
        if min_required_size >= len(time_range):
            raise ValueError(f"X time range is smaller than minimal required {min_required_size}")
        
        test_start = len(time_range) - min_required_size
        for _ in range(self.n_splits):
            test_end = test_start + self.test_size

            train_time = time_range[:test_start]
            test_time = time_range[test_start:test_end]

            train_indices = time_idx.isin(train_time)
            test_indices = time_idx.isin(test_time)

            test_start += self.step_size

            yield np.where(train_indices)[0], np.where(test_indices)[0]


    
    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits
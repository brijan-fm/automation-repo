from typing import List, Tuple

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, root_mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge


class BaseFactory:
    def __init__(self):
        self.pipeline = None
        self.features = None 

    def preprocessing(self, df, *args, **kwargs):
        raise NotImplemented 

    def initialize_pipeline(self, steps: List[Tuple]=None):
        """define sklearn pipeline instance.

        Parameters
        ----------
        steps : List[Tuple], optional
            Tuples that describe the sequence of action taken during train and fit in pipeline, by default None
            steps = [('scaler', StandardScaler()), ('svc', SVC())]
        """
        self.pipeline = Pipeline(steps)

    def train(self, X: pd.DataFrame, y: pd.Series, *args, **kwargs):
        if self.pipeline is None:
            self.initialize_pipeline()
        self.target = y.name 
        self.pipeline.fit(X, y, *args, **kwargs)

    def predict(self, X: pd.DataFrame, est=None, *args, **kwargs):
        if est is None:
            est = self.pipeline
        return est.predict(X, *args, **kwargs)

    def cross_validate(self, X, y, *args, **kwargs):
        raise NotImplementedError


class SalesPredictionFactory(BaseFactory):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def preprocessing(self, df, *args, **kwargs):
        df = df.copy()
        df.columns = [col.lower() for col in df.columns]
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df['year_week'] = df['date'].dt.year * 100 + df['date'].dt.isocalendar().week
        df.set_index(['store', 'year_week'], inplace=True)
        df.drop(columns='date', inplace=True)
        df.sort_index()
        return df
    
    def initialize_pipeline(
            self, 
            steps = None,
            cols_to_scale: List[str] | None = None,
            features_list: List[str] | None = None,
        ):
        if steps is None:
            steps = [
                ("column_transformer", ColumnTransformer(
                    [
                        ("numerical_scaler", StandardScaler(), cols_to_scale)
                    ]
                )),
                ("model", LinearRegression())
            ]
        super().initialize_pipeline(steps=steps)

    def cross_validate(self, X, y, return_results, return_eval_df, *args, **kwargs):
        self.results = cross_validate(self.pipeline, X, y, return_estimator=True, return_indices=True, *args, **kwargs)

        eval_dfs, summary_metric_list = [], []

        for idx, (est, indices) in enumerate(zip(self.results['estimator'], self.results['indices']['test'])):
            eval_df = y.iloc[indices].to_frame(name='true')
            eval_df['pred'] = self.predict(X.iloc[indices], est=est)
            eval_df['fold'] = idx + 1

            metric_summary = {
                'mae': mean_absolute_error(eval_df['true'], eval_df['pred']),
                'mse': mean_squared_error(eval_df['true'], eval_df['pred']),
                'mape': mean_absolute_percentage_error(eval_df['true'], eval_df['pred']),
                'rmse': root_mean_squared_error(eval_df['true'], eval_df['pred']),
            }
            eval_dfs.append(eval_df)
            summary_metric_list.append(metric_summary)
        summary_metric_df = pd.DataFrame(summary_metric_list).T 
        summary_metric_df['avg'] = summary_metric_df.mean(axis=1)


        cv_output = {
            'metric_summary': summary_metric_df
        }

        if return_results:
            cv_output['results'] = self.results
        
        if return_eval_df:
            cv_output['eval_df'] = eval_dfs

        return cv_output
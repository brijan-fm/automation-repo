import numpy as np
import pandas as pd 

from src.mlflow_demo.factory import SalesPredictionFactory
from src.mlflow_demo.utils.model_selection import TimeBasedSplit



df = pd.read_csv('data/walmart_sales.csv')
target = 'weekly_sales'
cols_to_scale = ['temperature', 'fuel_price', 'cpi', 'unemployment']


factory = SalesPredictionFactory(target=target)
factory.initialize_pipeline(
    cols_to_scale=cols_to_scale
)

transformed_df = factory.preprocessing(df)
X = transformed_df.drop(columns=target)
y = transformed_df[target]

results = factory.cross_validate(X, y, cv=TimeBasedSplit(n_splits=4, test_size=8, step_size=4, time_idx_name='year_week'), return_results=True, return_eval_df=True)
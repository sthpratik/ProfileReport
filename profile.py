import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('diabetes_dataset.csv')
profile = ProfileReport(df, title="Profiling Report")

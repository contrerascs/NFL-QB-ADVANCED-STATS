import pandas as pd

def load_datasets():
    qb_complete_df = pd.read_csv('data/qb_complete_stats.csv')
    return qb_complete_df
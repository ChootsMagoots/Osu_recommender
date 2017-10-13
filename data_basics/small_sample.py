import pandas as pd

users_df = pd.read_csv('data/users.csv')

users_slice = users_df.iloc[0:1000]

user_recent_df = pd.read_csv('data/user_recent.csv')

user_recent_slice = user_recent_df.iloc[0:1000]

user_recent_slice.to_csv('data_sample/user_recent_sample.csv')

users_slice.to_csv('data_sample/users_sample.csv')
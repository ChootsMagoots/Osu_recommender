import pymongo
import pandas as pd

mongodb_uri = None
mc = pymongo.MongoClient(mongodb_uri)  # Create MongoClient instance
db = mc['osu_data']  # Specify the database to work with
user = db['user']  # Specify the collection name to work with
user_best = db['user_best']
user_recent = db['user_recent']
beatmaps = db['beatmaps']

user_df = pd.DataFrame(list(user.find()))
user_best_df = pd.DataFrame(list(user_best.find()))
user_recent_df = pd.DataFrame(list(user_recent.find()))
beatmaps_df = pd.DataFrame(list(beatmaps.find()))

print('data loaded')

user_df.to_csv(path_or_buf = 'data/users.csv')
print('user_df to csv done')
user_best_df.to_csv(path_or_buf = 'data/user_best.csv')
print('user_best to csv done')
user_recent_df.to_csv(path_or_buf = 'data/user_recent.csv')
print('user_recent to csv done')
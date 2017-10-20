from sklearn.model_selection import train_test_split
import pandas as pd

filename = input("Please enter the filename: ")

df = pd.read_csv(filename)

train, test = train_test_split(df, test_size = 0.2)

train.to_csv("train" + filename)

test.to_csv("test" + filename)
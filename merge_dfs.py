import os
import pandas as pd

frames = [pd.read_csv(df) for df in os.listdir() if 'fake_users' in df]
frames = pd.concat(frames)

frames.to_csv('ALL_USERS.csv')

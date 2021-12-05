import pandas as pd
leaderboard_file = 'static/leaderboard.csv'

df = pd.read_csv(leaderboard_file)
f=pd.Timestamp(df['timestamp'])
print(f)
# df['timestamp']=df['timestamp'].date()
p=df['timestamp']
print(p)


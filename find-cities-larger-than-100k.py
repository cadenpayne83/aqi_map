import pandas as pd

df = pd.read_csv('uscities.csv')
filtered_df = df[df['population'] >= 100000]
filtered_df.to_csv('us_cities_100k_plus.csv', index=False)

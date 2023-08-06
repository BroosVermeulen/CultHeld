import pandas as pd


df_paradiso = pd.read_csv('paradiso.csv')
df_studiok = pd.read_csv('studiok.csv')
df_de_balie = pd.read_csv('de_balie.csv')

df = pd.concat([df_paradiso, df_studiok, df_de_balie])

df.to_csv('combined_venues.csv', encoding='utf-8')

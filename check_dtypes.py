import pandas as pd

df = pd.read_csv('chicago_crime_complete_daily_enhanced_FIXED.csv', nrows=10)
print('Data types:')
for col in df.columns:
    print(f'{col}: {df[col].dtype}')

print('\nFirst few rows:')
print(df.head(2))

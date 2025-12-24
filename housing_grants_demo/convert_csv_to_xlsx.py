import pandas as pd

# Read the semicolon-separated CSV
df = pd.read_csv('grants.csv', sep=';', encoding='utf-8')

# Export to clean Excel
df.to_excel('cyprus_grants_best.xlsx', index=False)

print("Converted successfully to 'cyprus_grants_best.xlsx'!")
print(f"Total rows: {len(df)} (including header)")
import pandas as pd
import sqlite3

# Step 1: Read the CSV file
# The file uses ';' as separator and has some empty/bad lines
df = pd.read_csv('input.csv', sep=';', on_bad_lines='skip')

# Optional: Clean up – drop completely empty rows (all NaN)
df = df.dropna(how='all')

# Convert columns to appropriate types (optional but recommended)
df['funding_amount'] = pd.to_numeric(df['funding_amount'], errors='coerce').astype('Int64')  # Nullable integer
# date_created remains as string/object, fine for SQLite

print("DataFrame preview:")
print(df)
print("\nNumber of rows to insert:", len(df))

# Step 2: Connect to SQLite database (creates 'my_database.db' if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Step 3: Create table if it doesn't exist
conn.execute('''
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_name TEXT,
    logo_URL TEXT,
    available_calls TEXT,
    funding_amount INTEGER,
    date_created TEXT
);
''')

# Step 4: Insert data (only non-null rows)
# Using pandas to_sql is the easiest way – it handles NaN as NULL
df.to_sql('entities', conn, if_exists='append', index=False)

# Commit and close
conn.commit()
conn.close()

print("\nData successfully imported into 'my_database.db' table 'entities'!")
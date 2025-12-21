import pandas as pd
import sqlite3

# Step 1: Read the CSV file
# The file uses ';' as separator and has some empty lines
df = pd.read_csv('input.csv', sep=';', on_bad_lines='skip')

# Step 1.2: Clean up / drop completely empty rows
df = df.dropna(how='all')

# Step 1.3 (optional): Convert columns to appropriate types
df['funding_amount'] = pd.to_numeric(df['funding_amount'], errors='coerce').astype('Int64') #null integer
# date_created remains as string which is fine for SQLite

print("DataFrame preview:")
print(df)
print("\nNumber of rows to insert:", len(df))

# Step 2: Connect to SQLite database (creates 'my_database.db')
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
# Using pandas to_sql
df.to_sql('entities', conn, if_exists='append', index=False)

# Commit and close
conn.commit()
conn.close()


print("\nData successfully imported into 'my_database.db' table 'entities'!")

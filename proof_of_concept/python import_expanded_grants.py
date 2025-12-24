import pandas as pd
import sqlite3

# Step 1: Read the new Cyprus CSV
cyprus_df = pd.read_csv('res_fund_grants_expanded.csv', sep=';', encoding='utf-8')

# Step 2: Create a sample Malta row to match your original example
malta_data = {
    'country': ['Malta'],
    'entity_name': ['Housing Authority'],
    'logo_url': ['https://wrkddbzhypcgbzpdliya.supabase.co/storage/v1/object/public/public-assets/entity-logos/housing-authority.png'],
    'available_calls': ['First-time buyer scheme'],
    'beneficiaries': ['Individuals'],
    'funding_amount': ['A €10,000 grant given over a period of 10 years after purchasing your first home.'],
    'funding_type': ['Grant'],
    'eligibility_criteria': ['a. 2022 Property purchased after January 2022\nb. >18 Age\nc. 1° Residential property'],
    'open_date': ['Open'],
    'close_date': ['Ongoing'],
    'application_requirements': [''],
    'call_links': ['https://housingauthority.gov.mt/scheme/first-time-buyer-scheme/'],
    'trigger_website': ['https://housingauthority.gov.mt/schemes/'],
    'date_created': ['2025-01-01'],
    'date_updated': ['']
}
malta_df = pd.DataFrame(malta_data)

# Step 3: Combine both data sets
combined_df = pd.concat([malta_df, cyprus_df], ignore_index=True)

print("Combined data preview:")
print(combined_df)
print(f"\nTotal rows: {len(combined_df)}")

# Step 4: Connect to SQLite and import
conn = sqlite3.connect('grants_database.db')  # New database name to avoid confusion

# Create table with all columns (TEXT for flexibility, since some fields have long text)
conn.execute('''
CREATE TABLE IF NOT EXISTS grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT,
    entity_name TEXT,
    logo_url TEXT,
    available_calls TEXT,
    beneficiaries TEXT,
    funding_amount TEXT,
    funding_type TEXT,
    eligibility_criteria TEXT,
    open_date TEXT,
    close_date TEXT,
    application_requirements TEXT,
    call_links TEXT,
    trigger_website TEXT,
    date_created TEXT,
    date_updated TEXT
);
''')

# Import the combined data
combined_df.to_sql('grants', conn, if_exists='replace', index=False)  # 'replace' to overwrite cleanly

conn.commit()
conn.close()

print("\nAll data successfully imported into 'grants_database.db' → table 'grants'!")

print("You now have Malta + Cyprus grants in one beautiful database.")

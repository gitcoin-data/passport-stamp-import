import os
import random
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Database connection details
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Create engine
engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

# Read the CSV file
df_csv = pd.read_csv('registry_stamp.csv')

# Get a list of unique ids from the csv
csv_ids = df_csv['id'].unique()

# Randomly select 1000 ids
random_ids = random.sample(list(csv_ids), 1000)

# Convert numpy.int64 to int
random_ids = [int(id) for id in random_ids]

# Query the database for these 1000 ids
query = "SELECT * FROM passport.registry_stamp WHERE id IN %s"
with engine.connect() as connection:
    df_db = pd.read_sql(query, params=(tuple(random_ids),), con=connection)

# Ensure that both dataframes are sorted in the same way
df_csv.set_index('id', inplace=True)
df_db.set_index('id', inplace=True)
df_csv.sort_index(inplace=True)
df_db.sort_index(inplace=True)

# Now, compare the 'hash' columns of the dataframes for the selected ids
comparison_hash = df_csv.loc[random_ids, 'hash'].equals(
    df_db.loc[random_ids, 'hash'])

if comparison_hash:
    print("The 'hash' columns of the two dataframes for the selected ids are identical.")
else:
    print("The 'hash' columns of the two dataframes for the selected ids are not identical.")

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import json
import ast
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

# Define chunk size
chunksize = 10 ** 3  # adjust this value depending on your available memory

print("loading file...")
# df = pd.read_csv('registry_stamp.csv', index_col='id')
# print("fixing json...")
# df['credential'] = df['credential'].apply(lambda x: json.dumps(ast.literal_eval(x)))
#
# print("inserting rows...")
# df.to_sql('registry_stamp', con=engine, schema="passport", if_exists='append', chunksize=1000)


c = 1
for chunk in pd.read_csv('registry_stamp.csv', index_col="id", chunksize=chunksize):
    print("fixing json...")
    chunk['credential'] = chunk['credential'].apply(
        lambda x: json.dumps(ast.literal_eval(x)))

    print("inserting rows...")
    chunk.to_sql('registry_stamp', con=engine, schema="passport",
                 if_exists='append', index=False)
    print(f"inserted  {c * chunksize}")
    c = c + 1

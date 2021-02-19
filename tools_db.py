import psycopg2
from psycopg2.extensions import AsIs

conn = psycopg2.connect("dbname=cabo_test user=postgres host=vm-03")
conn.set_session(autocommit=True)
cur = conn.cursor()

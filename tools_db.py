import psycopg2
import logs as LO
import parameters as PA


def get_access_to_db():
  try:
    conn = psycopg2.connect("dbname="+PA.DatabaseName+" user="+PA.DatabaseUser+" host="+PA.DatabaseHostName)
    conn.set_session(autocommit=True)
    return conn
  except Exception as err:
    LO.l_war('Unable to connect to the db')
    LO.l_war("Exception TYPE:", type(err))
    LO.l_war("Error:", err)
    LO.l_war("Connexion TYPE dbname="+PA.DatabaseName+" user="+PA.DatabaseUser+" host="+PA.DatabaseHostName, type(err))

def query_to_db(conn, query, val):
	touched = True
	with conn.cursor() as cur:
		try:
			cur.execute(query, val)
			if cur.rowcount == 0:
				touched = False
		except psycopg2.OperationalError as e:
			LO.l_err('Unable to connect! : ', e)
			LO.l_err('query >'+query)
			LO.l_err('val >'+val)
	return touched

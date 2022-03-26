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
    LO.l_war("Exception TYPE: {}".format(type(err)))
    LO.l_war("Error: {}".format(err))
    LO.l_war("Connexion TYPE dbname={} user={} host={} Error_Type: {}".format(PA.DatabaseName,PA.DatabaseUser,PA.DatabaseHostName,type(err)))

def query_to_db(conn, query, val):
  touched = False
  with conn.cursor() as cur:
    try:
      cur.execute(query, val)
      if cur.rowcount > 0:
        touched = True
      else:
        LO.l_war('DB warning\nNo row Touched: {}'.format(e))
        show_query(query,val)
    except psycopg2.OperationalError as e:
      LO.l_err('DB ERROR\nUnable to connect! : {}'.format(e))
      show_query(query,val)

    except psycopg2.InternalError as e:
      LO.l_err('DB ERROR\nInternal Error! : {}'.format(e))
      show_query(query,val)

    except psycopg2.DataError as e:
      LO.l_err('DB ERROR\nDataError! : {}'.format(e))
      show_query(query,val)

    except psycopg2.ProgrammingError as e:
      LO.l_err('DB ERROR\nProgrammingError! : {}'.format(e))
      show_query(query,val)

    except psycopg2.DatabaseError as e:
      LO.l_err('DB ERROR\nDatabaseError! : {}'.format(e))
      show_query(query,val)

    except psycopg2.NotSupportedError as e:
      LO.l_err('DB ERROR\nNotSupportedError! : {}'.format(e))
      show_query(query,val)

    except psycopg2.IntegrityError as e:
      LO.l_err('DB ERROR\nIntegrityError! : {}'.format(e))
      show_query(query,val)

  return touched
  
def show_query(query,val):
  LO.l_err('## DB ERROR => query >{}'.format(query))
  LO.l_err('## DB ERROR => val >{}'.format(val))

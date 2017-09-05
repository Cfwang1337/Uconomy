import psycopg2


def connect_with_onet():
    #onet DB and data dictionary are available at https://www.onetcenter.org/database.html?p=2
    conn = psycopg2.connect("dbname='onet' user='postgres' host='localhost' password='chaz1337'")
    cur = conn.cursor()
    return cur


def open_query(query):
    with open("queries/{0}.sql".format(query), 'rb') as query:
        cur = connect_with_onet()
        cur.execute(query.read())
        return cur.fetchall()


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
        output = cur.fetchall()
        cur.close()
        return output


def open_query_format(query, query_filter):
    with open("queries/{0}.sql".format(query), 'rb') as query:
        filtered_query = query.read().format(query_filter)
        cur = connect_with_onet()
        cur.execute(filtered_query)
        output = cur.fetchall()
        cur.close()
        return output

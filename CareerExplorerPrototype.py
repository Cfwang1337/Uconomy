import psycopg2


def connect_with_onet():
    #onet DB is from https://www.onetcenter.org/database.html?p=2
    conn = psycopg2.connect("dbname='onet' user='postgres' host='localhost' password='chaz1337'")
    cur = conn.cursor()
    return cur


def work_activities_query():
    with open("WorkActivities.sql", 'rb') as query:
        query_string = query.read()
        cur = connect_with_onet()
        cur.execute(query_string)

        rows = cur.fetchall()
        for row in rows[:10]:
            print row


def main():

    print "Please choose a survey"
    print "0. Work Activities"
    choice = raw_input ("ENTER A CHOICE: ")
    if choice == "0":
        work_activities_query()
    else:
        print "NOT AVAILABLE"
        exit()


if __name__ == "__main__":
    main()
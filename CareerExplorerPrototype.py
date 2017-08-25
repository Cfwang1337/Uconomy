import psycopg2


WORK_ACTIVITIES_QUESTIONS = [
    "I want to do something physically demanding",
    "I want to do something that requires keen senses and observation",
    "I want to solve problems",
    "I want to do something artistic or creative",
    "I want to heal and care for people",
    "I want to teach and mentor people",
    "I want to persuade people",
    "I want to lead people",
    "I want to use machines",
    "I want to fix and maintain machines",
    "I want to work with computers",
    "I want to operate heavy machinery and vehicles",
]


def connect_with_onet():
    #onet DB and data dictionary are available at https://www.onetcenter.org/database.html?p=2
    conn = psycopg2.connect("dbname='onet' user='postgres' host='localhost' password='chaz1337'")
    cur = conn.cursor()
    return cur


def work_activities_query():
    with open("WorkActivities.sql", 'rb') as query:
        cur = connect_with_onet()
        cur.execute(query.read())
        return cur.fetchall()


def work_activities_questionnaire():
    user_responses = []
    print "AGREE WITH THE FOLLOWING, ON A SCALE OF 1 to 5 (1 - completely disagree, 3 - indifferent, 5 - completely agree)"
    for question in WORK_ACTIVITIES_QUESTIONS:
        print ""
        response = raw_input("{0} ".format(question))
        while response not in ["1", "2", "3", "4", "5"]:
            response = raw_input(question)
        user_responses.append(int(response))

    return user_responses


def work_activities_scores():
    all_occupation_rankings = []
    user_responses = work_activities_questionnaire()
    comparisons = work_activities_query()
    for occupation in comparisons:
        ranking = 0
        for numb in range(0, len(user_responses)):
            if 0 <= occupation[numb + 3] < 0.2 and user_responses[numb] >= 1:
                ranking += 0
            if 0.2 <= occupation[numb + 3] < 0.4 and user_responses[numb] >= 2:
                ranking += 1
            if 0.4 <= occupation[numb + 3] < 0.6 and user_responses[numb] >= 3:
                ranking += 10
            if 0.6 <= occupation[numb + 3] < 0.8 and user_responses[numb] >= 4:
                ranking += 50
            if .8 <= occupation[numb + 3] <= 1 and user_responses[numb] >= 5:
                ranking += 250

        all_occupation_rankings.append([occupation[0], occupation[1], ranking])

    all_occupation_rankings = sorted(all_occupation_rankings, key=lambda x: x[-1], reverse=True)
    return all_occupation_rankings


#TODO NEED TO MODULARIZE WITH A MASTER MODULE, TO IMPORT PACKAGES
#TODO NEED TO REFACTOR SQL TO MAKE QUESTIONS MORE GRANULAR
#TODO NEED TO ACQUIRE OES AND COMPENSATION DATA
#TODO NEED TO BE ABLE TO MERGE RESULTS FROM MULTIPLE MODELS
def main():
    full_results = []
    print "Please choose a survey"
    print "0. Work Activities"
    print "1. Interests"
    print "2. Near Me"
    choice = raw_input ("ENTER A CHOICE: ")
    if choice == "0":
        results = work_activities_scores()
        full_results.append(results)

    for sub_result in full_results:
        for result in sub_result[:25]:
            print result

    else:
        print "NOT AVAILABLE YET"
        exit()


if __name__ == "__main__":
    main()
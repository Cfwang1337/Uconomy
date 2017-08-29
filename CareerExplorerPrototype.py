#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
import psycopg2


START_TIME = datetime.now().time().isoformat()


INPUT_TEXT = """
Find occupational recommendations based on the following:
0. Activities I Like
1. My Interests
2. My Skills, Knowledge, and Ability
3. My Personality and Behavior
4. Risks and Dangers I'm Willing To Accept
5. My Degree
6. My County, City, State, or Region

"Q" to tabulate results and exit
"""

#TODO STORE QUESTIONS ELSEWHERE
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


INTERESTS_QUESTIONS = [
    "I am very realistic and interested in tangible, concrete things",
    "I am very curious and interested in solving puzzles",
    "I am very artistic and interested in creative, expressive pursuits",
    "I am very nurturing and interested in helping people",
    "I am very enterprising and interested in leading projects",
    "I am very conscientious and interested in keeping things stable and orderly"
]


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


def questionnaire(questions):
    user_responses = []
    print "AGREE WITH THE FOLLOWING, ON A SCALE OF 1 to 5 (1 - completely disagree, 3 - indifferent, 5 - completely agree)"
    for question in questions:
        print ""
        response = raw_input("{0} ".format(question))
        while response not in ["1", "2", "3", "4", "5"]:
            response = raw_input(question)
        user_responses.append(int(response))

    return user_responses


def scoring(query, questions):
    all_occupation_rankings = []

    user_responses = questionnaire(questions)
    comparisons = open_query(query)

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


def make_choice():
    choice = raw_input(INPUT_TEXT)
    quitter(choice)
    while int(choice) not in range(0, 7):
        print "Please enter a valid choice"
        choice = raw_input(INPUT_TEXT)
        # quitter(choice)
    return choice


def quitter(choice):
    if choice == "Q" or choice == "q":
        print("QUITTING AND TABULATING RESULTS")
        print "Start time: {0} ".format(START_TIME)
        print "End time: {0}".format(datetime.now().time().isoformat())
        exit()


#TODO NEED TO MODULARIZE WITH A MASTER MODULE, TO IMPORT PACKAGES
#TODO NEED TO REFACTOR SQL TO MAKE QUESTIONS MORE GRANULAR
#TODO NEED TO ACQUIRE OES AND COMPENSATION DATA
#TODO NEED CENSUS DATA SHOWING CROSSWALK OF MAJORS AND OCCUPATIONS
def main():

    full_results = []

    results_df = pd.DataFrame(columns=["onet_score", "title", "rank_score"])

    if results_df.empty:
        print "empty"

    choices_made = []
    choice = make_choice()
    while str(choice).lower() != "q" and choice not in choices_made:
        if choice == "0":
            results = scoring("WorkActivities", WORK_ACTIVITIES_QUESTIONS)
        elif choice == "1":
            results = scoring("Interests", INTERESTS_QUESTIONS)
        else:
            choice == "q"
        #TODO COMBINATION LOGIC TO BE REPRESENTED HERE
        if results_df.empty:
            results_df.empty = pd.DataFrame(results, columns=["onet_score", "title", "rank_score"])
        else:
            results_temp = pd.DataFrame(results, columns=["onet_score", "title", "rank_score"])
            results_df.empty = pd.results_df.merge(results_temp, how="outer")

        # full_results.append(results)
        choices_made.append(choice)
        choice = make_choice()

    #TODO COMBINATION LOGIC
    full_results = list(results_df.values.values)
    for sub_result in full_results:
        for result in sub_result[:25]:
            print result
    quitter("q")

    #TODO NEED TO BE ABLE TO MERGE RESULTS FROM MULTIPLE MODELS
    #TODO NEED MECHANISM FOR RETURNING/PERSISTING


if __name__ == "__main__":
    main()
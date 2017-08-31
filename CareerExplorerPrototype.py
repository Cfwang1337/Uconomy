#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from helpers.helpers import open_query
from questions.questions import START_TIME, INPUT_TEXT, WORK_ACTIVITIES_QUESTIONS, INTERESTS_QUESTIONS
import pandas as pd


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

    return all_occupation_rankings


def make_choice():
    choice = raw_input(INPUT_TEXT)

    while choice.lower() != "q" and choice not in [str(x) for x in range(0, 7)]:
        print "Please enter a valid choice"
        choice = raw_input(INPUT_TEXT)
    return choice


def quitter(choice):
    if choice.lower() == "q":
        print("QUITTING AND TABULATING RESULTS")
        print "Start time: {0} ".format(START_TIME)
        print "End time: {0}".format(datetime.now().time().isoformat())
        exit()


def make_or_append_df(reference_df, results, column_name):
    if reference_df.empty:
        reference_df = pd.DataFrame(results, columns=["onet_score", "title", "{0}Score".format(column_name)])
    else:
        results_temp = pd.DataFrame(results, columns=["onet_score", "title", "{0}Score".format(column_name)])
        reference_df = reference_df.merge(results_temp, how="outer", on=["onet_score", "title"])
    return reference_df


#TODO NEED TO REFACTOR SQL TO MAKE QUESTIONS MORE GRANULAR
#TODO NEED TO ACQUIRE OES AND COMPENSATION DATA
#TODO NEED CENSUS DATA SHOWING CROSSWALK OF MAJORS AND OCCUPATIONS
def main():

    results_df = pd.DataFrame(columns=["onet_score", "title", "rank_score"])

    choices_made = []
    choice = make_choice()
    while str(choice).lower() != "q" and choice not in choices_made:
        if choice == "0":
            results = scoring("WorkActivities", WORK_ACTIVITIES_QUESTIONS)
            results_df = make_or_append_df(results_df, results, "WorkActivities")

            choices_made.append(choice)
            choice = make_choice()

        elif choice == "1":
            results = scoring("Interests", INTERESTS_QUESTIONS)
            results_df = make_or_append_df(results_df, results, "Interests")

            choices_made.append(choice)
            choice = make_choice()

        else:
            choice = make_choice()

    if not results_df.empty:
        result_columns = results_df.columns.values
        result_columns = [item for item in result_columns if "Score" in item]

        #TODO SUGGEST ALLOWING WEIGHTING AND OTHER WAYS TO TWEAK ANSWERS
        results_df['rank_score'] = 0

        for column in result_columns:
            results_df['rank_score'] = results_df['rank_score'] + results_df[column]

        full_results = results_df.sort_values(['rank_score'], ascending=0)

        print full_results[:25]

        full_results.to_csv("results/{0}.csv".format(datetime.now().isoformat()))

    quitter("q")


if __name__ == "__main__":
    main()
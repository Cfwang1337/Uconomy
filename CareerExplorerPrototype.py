#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from helpers.helpers import open_query, open_query_format
from questions.questions import START_TIME, INPUT_TEXT, WORK_ACTIVITIES_QUESTIONS, INTERESTS_QUESTIONS, SKA_QUESTIONS, \
    INDUSTRY_QUESTIONS, INDUSTRIES
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
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


def scoring(comparisons, questions):
    all_occupation_rankings = []

    user_responses = questionnaire(questions)

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


def ska_transform():
    ska_list = open_query("SkillsKnowledgeAbilities")

    data_list = pd.DataFrame([item[3:] for item in ska_list])

    data_list_std = StandardScaler().fit_transform(data_list)

    std_df = pd.DataFrame(data_list_std, index=[(item[:3]) for item in ska_list])

    pca_std = PCA(n_components=7)
    pca_std.fit_transform(data_list_std)

    identity = np.identity(data_list.shape[1])
    coef = pca_std.transform(identity)

    coef_df = pd.DataFrame(coef, columns=['Critical Thinking',
                                          'Service Orientation',
                                          'STEM',
                                          'Organizational Skill',
                                          'Situational Awareness',
                                          'General Knowledge',
                                          'Aesthetic Sense',
                                          ])

    dot_product = std_df.dot(coef_df)
    normalized_dot_product = MinMaxScaler().fit_transform(dot_product)
    multi_index = pd.MultiIndex.from_tuples([(item[:3]) for item in ska_list], names=["onetsoc_code", "title",                                                                                      "description"])
    normalized_dot_product = pd.DataFrame(normalized_dot_product, columns=list(dot_product), index=multi_index)

    return normalized_dot_product.reset_index().values.tolist()


def industry_transform():

    industry_choice = choose_industry()
    print industry_choice
    industry_list = open_query_format("Industry", industry_choice)
    return [[item[0], item[1], item[2]] for item in industry_list]


def choose_industry():

    print INDUSTRY_QUESTIONS

    print "PLEASE CHOOSE VALID VALUES UNDER 20. TYPE Q TO EXIT"
    industry_index = raw_input()

    indices = []
    while industry_index.lower() != "q" and industry_index in [str(x) for x in range(0, 20)]:
        indices.append(int(industry_index))
        industry_index = raw_input()

    return str(tuple(list(set([INDUSTRIES[industry_index] for industry_index in indices]))))


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


#TODO NEED TO BE ABLE TO FILTER BY LEVEL OF EDUCATION
#TODO NEED TO REFACTOR SQL TO MAKE QUESTIONS MORE GRANULAR
#TODO NEED TO ACQUIRE OES AND COMPENSATION DATA
#TODO NEED CENSUS DATA SHOWING CROSSWALK OF MAJORS AND OCCUPATIONS
def main():

    results_df = pd.DataFrame(columns=["onet_score", "title", "rank_score"])

    choices_made = []
    choice = make_choice()
    while str(choice).lower() != "q" and choice not in choices_made:
        if choice == "0":
            comparisons = open_query("WorkActivities")
            results = scoring(comparisons, WORK_ACTIVITIES_QUESTIONS)
            results_df = make_or_append_df(results_df, results, "WorkActivities")
            choices_made.append(choice)
            choice = make_choice()
        elif choice == "1":
            comparisons = open_query("Interests")
            results = scoring(comparisons, INTERESTS_QUESTIONS)
            results_df = make_or_append_df(results_df, results, "Interests")
            choices_made.append(choice)
            choice = make_choice()
        elif choice == "2":
            comparisons = ska_transform()
            results = scoring(comparisons, SKA_QUESTIONS)
            results_df = make_or_append_df(results_df, results, "Skills")
            choices_made.append(choice)
            choice = make_choice()
        #TODO LATER - SUPPORT MULTIPLE INDUSTRY CHOICES
        elif choice == "3":
            results = industry_transform()
            results_df = make_or_append_df(results_df, results, "Industry")
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

        print full_results[:25].to_string()

        full_results.to_csv("results/{0}.csv".format(datetime.now().isoformat()))

    quitter("q")


if __name__ == "__main__":
    main()
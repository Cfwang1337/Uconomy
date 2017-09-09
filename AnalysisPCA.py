#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from helpers.helpers import open_query
import math
import numpy as np
import pandas as pd


SKA_LIST = [
"Abilities - Cognitive Abilities - Category Flexibility",
"Abilities - Cognitive Abilities - Deductive Reasoning",
"Abilities - Cognitive Abilities - Flexibility of Closure",
"Abilities - Cognitive Abilities - Fluency of Ideas",
"Abilities - Cognitive Abilities - Inductive Reasoning",
"Abilities - Cognitive Abilities - Information Ordering",
"Abilities - Cognitive Abilities - Mathematical Reasoning",
"Abilities - Cognitive Abilities - Memorization",
"Abilities - Cognitive Abilities - Number Facility",
"Abilities - Cognitive Abilities - Oral Comprehension",
"Abilities - Cognitive Abilities - Oral Expression",
"Abilities - Cognitive Abilities - Originality",
"Abilities - Cognitive Abilities - Perceptual Speed",
"Abilities - Cognitive Abilities - Problem Sensitivity",
"Abilities - Cognitive Abilities - Selective Attention",
"Abilities - Cognitive Abilities - Spatial Orientation",
"Abilities - Cognitive Abilities - Speed of Closure",
"Abilities - Cognitive Abilities - Time Sharing",
"Abilities - Cognitive Abilities - Visualization",
"Abilities - Cognitive Abilities - Written Comprehension",
"Abilities - Cognitive Abilities - Written Expression",
"Abilities - Physical Abilities - Dynamic Flexibility",
"Abilities - Physical Abilities - Dynamic Strength",
"Abilities - Physical Abilities - Explosive Strength",
"Abilities - Physical Abilities - Extent Flexibility",
"Abilities - Physical Abilities - Gross Body Coordination",
"Abilities - Physical Abilities - Gross Body Equilibrium",
"Abilities - Physical Abilities - Stamina",
"Abilities - Physical Abilities - Static Strength",
"Abilities - Physical Abilities - Trunk Strength",
"Abilities - Psychomotor Abilities - Arm-Hand Steadiness",
"Abilities - Psychomotor Abilities - Control Precision",
"Abilities - Psychomotor Abilities - Finger Dexterity",
"Abilities - Psychomotor Abilities - Manual Dexterity",
"Abilities - Psychomotor Abilities - Multilimb Coordination",
"Abilities - Psychomotor Abilities - Rate Control",
"Abilities - Psychomotor Abilities - Reaction Time",
"Abilities - Psychomotor Abilities - Response Orientation",
"Abilities - Psychomotor Abilities - Speed of Limb Movement",
"Abilities - Psychomotor Abilities - Wrist-Finger Speed",
"Abilities - Sensory Abilities - Auditory Attention",
"Abilities - Sensory Abilities - Depth Perception",
"Abilities - Sensory Abilities - Far Vision",
"Abilities - Sensory Abilities - Glare Sensitivity",
"Abilities - Sensory Abilities - Hearing Sensitivity",
"Abilities - Sensory Abilities - Near Vision",
"Abilities - Sensory Abilities - Night Vision",
"Abilities - Sensory Abilities - Peripheral Vision",
"Abilities - Sensory Abilities - Sound Localization",
"Abilities - Sensory Abilities - Speech Clarity",
"Abilities - Sensory Abilities - Speech Recognition",
"Abilities - Sensory Abilities - Visual Color Discrimination",
"Knowledge - Arts and Humanities - English Language",
"Knowledge - Arts and Humanities - Fine Arts",
"Knowledge - Arts and Humanities - Foreign Language",
"Knowledge - Arts and Humanities - History and Archeology",
"Knowledge - Arts and Humanities - Philosophy and Theology",
"Knowledge - Business and Management - Administration and Management",
"Knowledge - Business and Management - Clerical",
"Knowledge - Business and Management - Customer and Personal Service",
"Knowledge - Business and Management - Economics and Accounting",
"Knowledge - Business and Management - Personnel and Human Resources",
"Knowledge - Business and Management - Sales and Marketing",
"Knowledge - Business and Management - Transportation",
"Knowledge - Communications - Communications and Media",
"Knowledge - Communications - Telecommunications",
"Knowledge - Education and Training - Education and Training",
"Knowledge - Engineering and Technology - Building and Construction",
"Knowledge - Engineering and Technology - Computers and Electronics",
"Knowledge - Engineering and Technology - Design",
"Knowledge - Engineering and Technology - Engineering and Technology",
"Knowledge - Engineering and Technology - Mechanical",
"Knowledge - Health Services - Medicine and Dentistry",
"Knowledge - Health Services - Therapy and Counseling",
"Knowledge - Law and Public Safety - Law and Government",
"Knowledge - Law and Public Safety - Public Safety and Security",
"Knowledge - Manufacturing and Production - Food Production",
"Knowledge - Manufacturing and Production - Production and Processing",
"Knowledge - Mathematics and Science - Biology",
"Knowledge - Mathematics and Science - Chemistry",
"Knowledge - Mathematics and Science - Geography",
"Knowledge - Mathematics and Science - Mathematics",
"Knowledge - Mathematics and Science - Physics",
"Knowledge - Mathematics and Science - Psychology",
"Knowledge - Mathematics and Science - Sociology and Anthropology",
"Skills - Complex Problem Solving Skills - Complex Problem Solving",
"Skills - Content - Active Listening",
"Skills - Content - Mathematics",
"Skills - Content - Reading Comprehension",
"Skills - Content - Science",
"Skills - Content - Speaking",
"Skills - Content - Writing",
"Skills - Process - Active Learning",
"Skills - Process - Critical Thinking",
"Skills - Process - Learning Strategies",
"Skills - Process - Monitoring",
"Skills - Resource Management Skills - Management of Financial Resources",
"Skills - Resource Management Skills - Management of Material Resources",
"Skills - Resource Management Skills - Management of Personnel Resources",
"Skills - Resource Management Skills - Time Management",
"Skills - Social Skills - Coordination",
"Skills - Social Skills - Instructing",
"Skills - Social Skills - Negotiation",
"Skills - Social Skills - Persuasion",
"Skills - Social Skills - Service Orientation",
"Skills - Social Skills - Social Perceptiveness",
"Skills - Systems Skills - Judgment and Decision Making",
"Skills - Systems Skills - Systems Analysis",
"Skills - Systems Skills - Systems Evaluation",
"Skills - Technical Skills - Equipment Maintenance",
"Skills - Technical Skills - Equipment Selection",
"Skills - Technical Skills - Installation",
"Skills - Technical Skills - Operation and Control",
"Skills - Technical Skills - Operation Monitoring",
"Skills - Technical Skills - Operations Analysis",
"Skills - Technical Skills - Programming",
"Skills - Technical Skills - Quality Control Analysis",
"Skills - Technical Skills - Repairing",
"Skills - Technical Skills - Technology Design",
"Skills - Technical Skills - Troubleshooting"]


def main():
    ska_list = open_query("SkillsKnowledgeAbilities")

    data_list = pd.DataFrame([item[3:] for item in ska_list])

    #STANDARD SCALE
    data_list_std = StandardScaler().fit_transform(data_list)

    std_df = pd.DataFrame(data_list_std, columns=SKA_LIST, index=[(item[:3]) for item in ska_list])
    std_df.to_csv("PCA_Standardized.csv")

    cov_mat = np.cov(data_list_std.T)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)

    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]
    print('Eigenvalues in descending order:')
    for i in eig_pairs:
        print(i[0])
    print ""

    pca_std = PCA(n_components=25)
    pca_std.fit_transform(data_list_std)
    for entry in pca_std.explained_variance_ratio_:
        print entry

    identity = np.identity(data_list.shape[1])
    coef = pca_std.transform(identity)

    coef_df = pd.DataFrame(coef, columns=['PC_1',
                                          'PC_2',
                                          'PC_3',
                                          'PC_4',
                                          'PC_5',
                                          'PC_6',
                                          'PC_7',
                                          'PC_8',
                                          'PC_9',
                                          'PC_10',
                                          'PC_11',
                                          'PC_12',
                                          'PC_13',
                                          'PC_14',
                                          'PC_15',
                                          'PC_16',
                                          'PC_17',
                                          'PC_18',
                                          'PC_19',
                                          'PC_20',
                                          'PC_21',
                                          'PC_22',
                                          'PC_23',
                                          'PC_24',
                                          'PC_25'
                                          ], index=SKA_LIST)
    print coef_df
    coef_df.to_csv("SKA_PCA.csv")

    #TODO DOT PRODUCT FOR COMPONENTS FOR EACH PROFESSION




if __name__ == "__main__":
    main()
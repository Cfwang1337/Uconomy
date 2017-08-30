from datetime import datetime

START_TIME = datetime.now().time().isoformat()

INPUT_TEXT = """
Find occupational recommendations based on the following:
0. Activities I Like
1. My Interests
2. My Skills, Knowledge, and Ability
3. My Personality and Values
4. Risks and Dangers I'm Willing To Accept
5. My Degree
6. My County, City, State, or Region

"Q" to tabulate results and exit
"""

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


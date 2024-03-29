"""
Program 9
-----------------------------------------------------------------------------------------------------------------------
Generate 1,00000 rows and put in csv file, synthesized data faculty data set where experience linearly mapped to designation, 
salary, no of publication, no of book chapters, amount of consultancy work, fund received, professional membership.
    A. Read csv file and load it into tuples (try lambda function)
    B. Perform the following operations:
        i. Using regular expression search for associate professors with more than 15 years experience, assistant Professors with more than 5 years experience, Professors with more than 20 years experience
        ii. Analyze the association rule mining of associate professors for their following performance relations in different contributions
            A. No. of publication and no of book chapters
            B. No. of publication and amount of consultancy work
            C. No. of publication and fund received
            D. No. of publication and professional membership
"""

import re
import os, csv
from random import randint, choice
from tqdm import tqdm
import pandas as pd

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from warnings import filterwarnings
filterwarnings("ignore")


def generate_faculty_data(num: int, filename: str) -> None:
    if filename in os.listdir(os.getcwd()):
        print("Dataset exists...")
    else:
        data = []
        data.append(['Experience', "Designation", "Salary", "Number of Publications", "Number of Chapters", "Amount of consultancy Work", "Fund Received", "Professional Membership"])
        designations = ["Assistant Professor", "Associate Professor", "Professor"]

        for i in tqdm(range(num)):
            designation = choice(designations)

            experience = randint(19, 40) if designation == "Professor" else (randint(8, 18) if designation == "Associate Professor" else randint(1, 7))

            salary = 50000 + 2000 * experience
            num_pub = int(experience * 1.5)
            num_chapters = int(experience / 3)
            amt_consultancy_work = experience * 1000
            fund_received = experience * 50000
            professional_membership = randint(2, 5)

            data.append([experience, designation, salary, num_pub, num_chapters, amt_consultancy_work, fund_received, professional_membership])

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)


def read_csv_as_tuple(file: str) -> tuple:
    with open(file, newline="") as f:
        read = csv.reader(f)
        data = tuple(map(lambda row: tuple(row), read))
        return data


def association_rule_mining(designation: str, experience: int) -> None:
    for tup in csv_tuple[:5]:
        if re.search(designation, tup[1]) != None and int(tup[0]) > experience:
            print(tup)

    print(f"\nAssociation Rules for {designation} with {experience} years experience:")

    for col in ['Number of Chapters', 'Amount of consultancy Work', 'Fund Received', 'Professional Membership']:
        df = pd.read_csv(dataset_file)
        
        designation_exp = df[(df['Designation'] == designation) & (df['Experience'] > experience)]
        
        data = designation_exp[['Number of Publications', col]]

        data_binary = data.applymap(lambda x: 1 if x > 0 else 0)

        frequent_itemsets = apriori(data_binary, min_support=0.1, use_colnames=True)

        association_rules_df = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

        print(f"Number of Publications and {col}:")
        print(association_rules_df)
        print()


dataset_file = "re_synthetic_faculty_dataset.csv"

generate_faculty_data(100000, dataset_file)

csv_tuple = read_csv_as_tuple(dataset_file)
print("\nFaculty Dataset as tuple imported using lambda function:\n")
print(csv_tuple[:5])


# Professor
association_rule_mining("Professor", 20)

# Associate Professor
association_rule_mining("Associate Professor", 15)

# Assistant Professor
association_rule_mining("Assistant Professor", 5)

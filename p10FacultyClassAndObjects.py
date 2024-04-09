"""
Program 10
------------------------------------------------------------------------------------------------------------------------------
Generate 100000 rows and put it in csv file, synthesized data faculty dataset where experience linearly mapped to designation,
salary, no. of publications, no. of chapters, amount of consultancy work, fund received and professional membership. 
Use classes and objects for the following operations:
i. Read csv file and load it into temp variables
ii. Perform the following operations
    a. Using lambda and regular expression to search for associate professors with more than 25 years experience and 
        load in another temp list called "asso_prof_25"
    b. In asso_prof_25 list do the following factoring:
        1. If experience > 25, yes means set the value as 1 else 0
        2. If publication count > 5, yes means set the value as 1 else 0
        3. Similarly do for no. of publications > 3, amount of consultancy work > 50000, fund received > 500000, 
            professional membership > 2
    c. Analyze the association rule mining of associate professors for the following performance relations in different contributions
        1. Experience, designation, no. of publications and no. of book chapters
        2. Experience, designation, no. of publications and amount of consultancy work
        3. Experience, designation, no. of publications and fund received
        3. Experience, designation, no. of publications and professional membership
"""

import os, csv, re
from random import randint, choice
from tqdm import tqdm
import pandas as pd

from mlxtend.frequent_patterns import association_rules, apriori
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

            experience = randint(25, 40) if designation == "Professor" else (randint(12, 29) if designation == "Associate Professor" else randint(1, 14))

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


class FacultyOperations:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

        with open(self.dataset_path, newline="") as f:
            read = csv.reader(f)
            data = list(map(lambda row: list(row), read))
            self.data = data
        
    def search(self, designation: str, experience: int) -> list:
        data_ls = []
        for ls in self.data[1:]:
            if re.search(designation, ls[1]) != None and int(ls[0]) > experience:
                data_ls.append(ls)
        
        return data_ls
    
    def factoring(self, data: list) -> list:
        res = []
        for d in data:
            temp = []
            temp.append(1 if int(d[0]) > 25 else 0)
            temp.append(d[1])
            temp.append(1 if int(d[3]) > 5 else 0)
            temp.append(1 if int(d[4]) > 3 else 0)
            temp.append(1 if int(d[5]) > 50000 else 0)
            temp.append(1 if int(d[6]) > 500000 else 0)
            temp.append(1 if int(d[7]) > 2 else 0)
            
            res.append(temp)

        return res
    

    def association_rule_mining(self, designation: str, experience: int) -> None:
        df = pd.read_csv(self.dataset_path)
        df["Designation"].replace("Assistant Professor", 0, inplace=True)
        df["Designation"].replace("Associate Professor", 1, inplace=True)
        df["Designation"].replace("Professor", 2, inplace=True)

        map_designation = {
            "Assistant Professor": 0,
            "Associate Professor": 1,
            "Professor": 2,
        }
        
        print(f"\nAssociation Rules for {designation} with {experience} years experience:")

        for col in ['Number of Chapters', 'Amount of consultancy Work', 'Fund Received', 'Professional Membership']:
            designation_exp = df[(df['Designation'] == map_designation[designation]) & (df['Experience'] > experience)]
            data = designation_exp[['Experience', "Designation", 'Number of Publications', col]]

            data_binary = data.applymap(lambda x: 1 if x > 0 else 0)
            frequent_itemsets = apriori(data_binary, min_support=0.1, use_colnames=True)
            association_rules_df = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

            print(f"Number of Publications and {col}:")
            print(association_rules_df)
            print()

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)

            association_rules_df.to_excel(f'association_rules_{designation}_{col}.xlsx', index=False)
            

dataset_file = "re2_synthetic_faculty_dataset.csv"

generate_faculty_data(100000, dataset_file)

faculty = FacultyOperations(dataset_file)
asso_prof_25 = faculty.search("Associate Professor", 25)
print(asso_prof_25[:10])

factor_res = faculty.factoring(asso_prof_25)
print(factor_res[:10]) 

faculty.association_rule_mining("Associate Professor", 25)

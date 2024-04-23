"""
Program 11
------------------------------------------------------------------------------------------------------------------------------
Create a csv file called "books.csv" with synthesized data set having the following columns: 
Student usn, semester-number, sub-code, subject name, book referred, book-id, grade scored.
    1. Use exception handling for file operations.
        i. Read the csv file content into local variables for accessing them in python
        ii. Extract only sem-number, sub-code, book-id and grade scored and store in another CSV file called "extracted-books.csv".
        iii. Note: When you write into the "extracted-books.csv", file Convert grade code to number (Sgrade-9, A grade-8,etc) 
            and update into the file
    2. Analyse the coorelation between sem-number, sub-code, book-id and grade scored
        i. Convert the data set in required format to perform association rule mining an analyse the output
        ii. Convert the data set in required format to Perform the collaboration filtering over the data set.
"""

import csv
from faker import Faker
import random
from tqdm import tqdm

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from mlxtend.frequent_patterns import association_rules, apriori
from surprise import Dataset, Reader, SVD

from warnings import filterwarnings
filterwarnings("ignore")

subjects = ["Maths", "ADBMS", "AIML", "VR", "IoT", "RMI"]

books = ["Advanced Mathematics", "Database Concepts", "AI & ML", "Virtual Reality", "IoT and its applications", "Reseach Methodology & IPR"]

def generate_books(filename: str, num_records: int) -> list:
    fake = Faker()

    data = []
    for _ in tqdm(range(num_records)):
        sem = 1
        sub = random.choice(subjects)
        sub_index = subjects.index(sub)
        sub_code = f"MCS{sem}{sub_index+1}"
        year_of_studying = 1 if sem in [1, 2] else 2
        usn = f"1MS{24-year_of_studying}CS{fake.random_int(min=1, max=10000)}"

        book_ref = books[sub_index]
        book_id = f"BID0{books.index(book_ref)+1}"

        grade = random.choice(["A", "B", "C", "D", "S"])

        data.append([usn, sem, sub_code, sub, book_ref, book_id, grade])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['USN', 'SEM', 'SUB_CODE', 'SUBJECT_NAME', 'BOOK_REFERRED', "BOOK_ID", "GRADE_SCORED"])
        writer.writerows(data)

    return data


def replace_grades_to_num(df):
    df["GRADE_SCORED"].replace("S", 9, inplace=True)
    df["GRADE_SCORED"].replace("A", 8, inplace=True)
    df["GRADE_SCORED"].replace("B", 7, inplace=True)
    df["GRADE_SCORED"].replace("C", 6, inplace=True)
    df["GRADE_SCORED"].replace("D", 5, inplace=True)

    return df


def association_rule_mining(df) -> None:
    data = df.copy()

    data_binary = data.applymap(lambda x: 1 if x > 0 else 0)

    frequent_itemsets = apriori(data_binary, min_support=0.1, use_colnames=True)

    association_rules_df = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

    print(f"Association Rules between SEM NUMBER, SUB-CODE, BOOK ID & GRADE SCORED:")
    print(association_rules_df)
    print()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    association_rules_df.to_excel(f'association_rules_sem_subcode_bookid_grade.xlsx', index=False)


def collaboration_filtering(df, sub_code: str) -> None:
    df_ratings = df.copy()

    reader = Reader(rating_scale=(8, 10))

    dataset = Dataset.load_from_df(metadata[["SUB_CODE", 'BOOK_ID', 'GRADE_SCORED']], reader)

    model = SVD()
    trainset = dataset.build_full_trainset()
    model.fit(trainset)

    items_to_ignore = df_ratings[df_ratings['SUB_CODE'] == sub_code]['BOOK_ID']  
    unrated_items = df_ratings[~df_ratings['BOOK_ID'].isin(items_to_ignore)]['BOOK_ID'].unique() 

    testset = [(0, book_id, 0) for book_id in unrated_items]

    predictions = model.test(testset)

    sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

    top_recommendations = [(pred.iid, pred.est) for pred in sorted_predictions[:10]]

    print(f"Top recommendations for subject code {sub_code}:")
    for book_id, predicted_rating in top_recommendations:
        print(f"Book ID: {book_id}, Predicted Rating: {predicted_rating}")


dataset_file = 'books.csv'
books_data = generate_books(dataset_file, 100000)

books_data[:10]

df = pd.read_csv(dataset_file)

extracted = df[["SEM", "SUB_CODE", "BOOK_ID", "GRADE_SCORED"]]
extracted = replace_grades_to_num(extracted)

extracted.to_csv("extracted-books.csv", index=False)

extracted_unit = pd.read_csv("extracted-books.csv", index_col=0)

for i, col in enumerate(["SUB_CODE", "BOOK_ID"]):
    if i == 0:
        for val in extracted[col]:
            extracted_unit[col].replace(val, int(val[-1]), inplace=True)
    else:
        for val in extracted[col]:
            extracted_unit[col].replace(val, int(val[-1]), inplace=True)


correlation = extracted_unit.corr()
sns.set(rc = {'figure.figsize':(10, 6)})
sns.heatmap(correlation, annot=True)
plt.title("Correlation Matrix HeatMap")
plt.show()

association_rule_mining(extracted_unit)

metadata = pd.read_csv("books.csv", low_memory=False)
metadata = replace_grades_to_num(metadata)

collaboration_filtering(metadata, "MSC11")

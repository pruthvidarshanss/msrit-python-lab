"""
Program 11
-----------------------------------------------------------------------------------------------------------------------------------
Create a csv file called "books.csv" with synthesized dataset having the following columns: 
Student usn, semester-number, sub-code, subject name, book referred, book-id, grade scored.
1. Use exception handling for file operations.
    i. Read the csv file content into local variables for accessing them in python
    ii. Extract only sem-number, sub-code, book-id and grade scored and store in another CSV file called "extracted-books.csv".
    iii. Note: When you write into the "extracted-books.csv", file Convert grade code to number (Sgrade-9, A grade-8,etc) 
        and update into the file
2. Analyse the coorelation between sem-number, sub-code, book-id and grade scored
    i. Convert the dataset in required format to perform association rule mining an analyse the output
    ii. Convert the dataset in required format to perform the collaboration filtering over the dataset.
"""

import csv, random
from faker import Faker
from tqdm import tqdm

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from mlxtend.frequent_patterns import association_rules, apriori
from sklearn.metrics.pairwise import cosine_similarity

from warnings import filterwarnings
filterwarnings("ignore")

subjects = ["Maths", "ADBMS", "AIML", "VR", "IoT", "RMI"]

cse_subjects_books = {
    "Advanced Mathematics" : (1, ["Probability and Statistics", "Probability & Statistics with Reliability, Queuing and Computer Science Applications", "Linear Algebra with Applications", "Advanced Engineering Mathematics"]), 
    "ADBMS": (2, ["Fundamentals of Database Systems", "Database System Concepts", "NoSQL for Mere Mortals"]), 
    "RMI": (3, ["Engineering Research Methodology", "Research Methods for Engineers"]),
    "VR": (4, ["Virtual Reality", "Virtual and Augmented Reality (VR/AR)"]), 
    "AIML": (5, ["Artificial Intelligence - A Modern Approach", "Machine Learning"]), 
    "IoT": (6, ["Internet of Things", "Designing the Internet of Things, Wiley"]), 
}

def generate_books(filename: str, num_records: int) -> list:
    fake = Faker()

    data = []
    for _ in tqdm(range(num_records)):
        sem = 1
        subject = random.choice(list(cse_subjects_books.keys()))
        sub_index, books = cse_subjects_books[subject]
        sub_code = f"MCS{sem}{sub_index+1}"
        year_of_studying = 1 if sem in [1, 2] else 2
        usn = f"1MS{24-year_of_studying}CS{fake.random_int(min=1, max=10000)}"

        book_ref = random.choice(books)
        book_id = f"BID{sub_index}{books.index(book_ref)+1}"

        grade = random.choice(["A", "B", "C", "D", "S"])

        data.append([usn, sem, sub_code, subject, book_ref, book_id, grade])

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


def recommend_books(book_id, user_item_matrix, item_similarity, top_n=10):
    similar_books = pd.Series(item_similarity[user_item_matrix.index == book_id][0], index=user_item_matrix.index)
    similar_books = similar_books.sort_values(ascending=False)
    similar_books = similar_books.drop(book_id)  
    return similar_books.head(top_n)


dataset_file = 'p11books.csv'
books_data = generate_books(dataset_file, 100000)

print(books_data[:10])

df = pd.read_csv(dataset_file)

extracted = df[["SEM", "SUB_CODE", "BOOK_ID", "GRADE_SCORED"]]
extracted = replace_grades_to_num(extracted)

extracted.to_csv("extracted-books.csv", index=False)

extracted_unit = pd.read_csv("extracted-books.csv", index_col=0)

for i, col in enumerate(["SUB_CODE", "BOOK_ID"]):
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

user_item_matrix = metadata.pivot_table(index='BOOK_ID', columns='SUB_CODE', values='GRADE_SCORED', fill_value=0)

item_similarity = cosine_similarity(user_item_matrix)

recommended_books = recommend_books('BID31', user_item_matrix, item_similarity)
print("Recommendation for Book ID: BID31")
print(recommended_books)

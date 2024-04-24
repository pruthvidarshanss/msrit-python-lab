"""
Program 12
-----------------------------------------------------------------------------------------------------------------------------------
Create a csv file called "books.csv" with synthesized dataset having the following columns: 
Student usn, semester-number, sub-code, subject name, book referred, book-id, grade scored.
   1. Read the csv file content into linked list for accessing them in python
   2. Extract only sem-number, sub-code, book-id and grade scored and store in another CSV file called "extracted-books.csv".
   3. Note: When you write into the "extracted-books.csv", file Convert grade code to number (Sgrade-9, A grade-8,etc) 
   and update into the file
   4. Analyse the coorelation between sem-number, sub-code, book-id and grade scored
      i. Convert the dataset in required format to perform the collaboration filtering over the dataset.
"""

import csv, random
from faker import Faker
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return
        else:
            cur_node = self.head
            while cur_node.next is not None:
                cur_node = cur_node.next

            cur_node.next = new_node


    def updateNode(self, val, index):
        current_node = self.head
        position = 0
        if position == index:
            current_node.data = val
        else:
            while(current_node != None and position != index):
                position = position+1
                current_node = current_node.next

            if current_node != None:
                current_node.data = val
            else:
                print("Index not present")


    def sizeOfLL(self):
        size = 0
        if self.head:
            current_node = self.head
            while current_node:
                size += 1
                current_node = current_node.next
            return size
        else:
            return 0

    def printLL(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next


    def getLL(self, index):
        cur_node = self.head
        pos = 0
        if pos == index:
            return cur_node.data
        else:
            while cur_node != None and pos != index:
                pos += 1
                cur_node = cur_node.next

            if cur_node != None:
                return cur_node.data
            else:
                print("Index not present")


cse_subjects_books = {
    "Advanced Mathematics" : (1, ["Probability and Statistics", "Probability & Statistics with Reliability, Queuing and Computer Science Applications", "Linear Algebra with Applications", "Advanced Engineering Mathematics"]), 
    "ADBMS": (2, ["Fundamentals of Database Systems", "Database System Concepts", "NoSQL for Mere Mortals"]), 
    "RMI": (3, ["Engineering Research Methodology", "Research Methods for Engineers"]),
    "VR": (4, ["Virtual Reality", "Virtual and Augmented Reality (VR/AR)"]), 
    "AIML": (5, ["Artificial Intelligence - A Modern Approach", "Machine Learning"]), 
    "IoT": (6, ["Internet of Things", "Designing the Internet of Things, Wiley"]), 
}


def save_to_csv(filename: str, cols: list, data: list) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(cols)
        writer.writerows(data)


def generate_books(filename: str, num_records: int) -> list:
    fake = Faker()

    book_ll = LinkedList()
    data = []
    for _ in tqdm(range(num_records)):
        sem = 1
        subject = random.choice(list(cse_subjects_books.keys()))
        sub_index, books = cse_subjects_books[subject]
        sub_code = f"MCS{sem}{sub_index}"
        usn = f"1MS23CS{fake.random_int(min=1, max=10000)}"

        book_ref = random.choice(books)
        book_id = f"BID{sub_index}{books.index(book_ref)+1}"

        grade = random.choice(["A", "B", "C", "D", "S"])

        book_ll.append([usn, sem, sub_code, subject, book_ref, book_id, grade])
        data.append([usn, sem, sub_code, subject, book_ref, book_id, grade])

    save_to_csv(filename, ['USN', 'SEM', 'SUB_CODE', 'SUBJECT_NAME', 'BOOK_REFERRED', "BOOK_ID", "GRADE_SCORED"], data)

    return book_ll

dataset_file = 'p12books.csv'
books_data_ll = generate_books(dataset_file, 1000)


extracted_books_ll = LinkedList()

extracted_data = []
for i in range(books_data_ll.sizeOfLL()):
    data = books_data_ll.getLL(i)
    sem = data[1]
    sub_code = data[2]
    book_id = data[-2]
    grade = 9 if data[-1] == "S" else (8 if data[-1] == "A" else (7 if data[-1] == "B" else (6 if data[-1] == "C" else 5)))

    extracted_books_ll.append([sem, sub_code, book_id, grade])

    extracted_data.append([sem, sub_code, book_id, grade])


save_to_csv("p12extracted-books.csv", ['SEM', 'SUB_CODE', "BOOK_ID", "GRADE_SCORED"], extracted_data)


corr_ls = []
for i in range(extracted_books_ll.sizeOfLL()):
    data = extracted_books_ll.getLL(i)

    sub_code = int(data[1][-1])
    book_id = int(data[2][-2:])

    corr_ls.append([data[0], sub_code, book_id, data[-1]])

save_to_csv("p12correlation-books.csv", ['SEM', 'SUB_CODE', "BOOK_ID", "GRADE_SCORED"], corr_ls)


corr_df = pd.read_csv("p12correlation-books.csv", index_col=0)

correlation = corr_df.corr()
sns.set(rc = {'figure.figsize':(10, 6)})
sns.heatmap(correlation, annot=True)
plt.title("Correlation Matrix HeatMap")
plt.show()


df = pd.read_csv("p12extracted-books.csv")

user_item_matrix = df.pivot_table(index='BOOK_ID', columns='SUB_CODE', values='GRADE_SCORED', fill_value=0)

item_similarity = cosine_similarity(user_item_matrix)

def recommend_books(book_id, user_item_matrix, item_similarity, top_n=10):
    similar_books = pd.Series(item_similarity[user_item_matrix.index == book_id][0], index=user_item_matrix.index)
    similar_books = similar_books.sort_values(ascending=False)
    similar_books = similar_books.drop(book_id)  
    return similar_books.head(top_n)

recommended_books = recommend_books('BID32', user_item_matrix, item_similarity)
print("Recommendation for Book ID: BID32")
print(recommended_books)
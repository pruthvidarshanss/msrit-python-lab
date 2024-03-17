"""
Program 8
-----------------------------------------------------------------------------------------------------------------------
Generate 100000 rows and put in csv file, sythesized faculty dataset where experience linearly mapped to designation,
salary, no. of publications, no. of chapters, amount of consultancy work, fund recieved, professional membership.

a. Read csv file and load it into tuple and Dictionary using Function, (try all the types of function)
b. Find out correlation among the fields in faculty dataset
c. Perform the following operations:
    i. Linear Regression analysis of following & plot the predicted value in separate graphs
    ii. KNN analysis of following & plot the predicted value in separate graphs
    iii. Apply Naiye Bayes algorithm for the following & plot the predicted value in separate graphs
            (x-axis - experience, y-axis - predicted value)
            I. No. of publication
            II. No. of Book chapters
            III. AMount of Consultancy work
            IV. Fund Received
            V. Professional Membership
"""


import os, csv
from random import randint
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


def generate_faulty_data(num: int, filename: str) -> None:
    if filename in os.listdir(os.getcwd()):
        print("Dataset exists...")
    else:
        data = []
        data.append(['Experience', "Designation", "Salary", "Number of Publications", "Number of Chapters", "Amount of consultancy Work", "Fund Received", "Professional Membership"])

        for i in tqdm(range(num)):
            experience = randint(1, 40)

            designation = 0 if experience < 7 else ( 1 if experience < 14 else 2 )

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
        data = [tuple(row) for row in read]
        data = tuple(data)

        return data


def read_csv_as_dict(file: str) -> dict:
    with open(file, newline="") as f:
        read = csv.reader(f)
        data = {}
        for i, d in enumerate(read):
            data[i] = d
		
        return data


def multiplot_model_pred(NAME: str, model):

    for i, val in enumerate(["Number of Publications", "Number of Chapters", "Amount of consultancy Work", "Fund Received", "Professional Membership"]):
        r = 0 if i < 2 else (1 if i < 5 else 2)
        c = 0 if i % 2 == 0 else 1
        cs = 2 if i == 4 else 1
        rs = 2 if i == 4 else 1

        plot = plt.subplot2grid((3, 2), (r, c), colspan=cs, rowspan=rs) 

        X = df[["Experience"]]
        Y = df[val]

        xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.2, random_state=99)

        model.fit(xTrain, yTrain)

        plot.scatter(xTest, yTest, color='blue')
        plot.plot(xTest, model.predict(xTest), color='red', linewidth=3)
        plot.set_title(f'Experience v/s {val}')
        
    plt.tight_layout()
    plt.show()


def plot_model_pred(NAME: str, TYPE: int, model) -> None:
    for val in ["Number of Publications", "Number of Chapters", "Amount of consultancy Work", "Fund Received", "Professional Membership"]:
        X = df[["Experience"]]
        Y = df[val]

        xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.2, random_state=99)

        model.fit(xTrain, yTrain)

        plt.figure(figsize=(10, 6))
        plt.scatter(xTest, yTest, color='blue')
        plt.plot(xTest, model.predict(xTest), color='red', linewidth=1) if TYPE == 0 else plt.scatter(xTest, model.predict(xTest), color='red', marker="*")
        plt.xlabel("Experience")
        plt.ylabel(val)
        plt.title(f'{NAME} Analysis: Experience v/s {val}')
        plt.show()


dataset_file = "ml_synthetic_faculty_dataset.csv"

generate_faulty_data(100000, dataset_file)

csv_tuple = read_csv_as_tuple(dataset_file)
print("\nFaculty Dataset as Tuple:\n")
print(csv_tuple[:5])


csv_dict = read_csv_as_dict(dataset_file)
print("\nFaculty Dataset as Dictionary:\n")
for i in range(5):
    print(f"{i} : {csv_dict[i]}")


# Correlation Matrix
df = pd.read_csv(dataset_file)
correlation = df.corr()

sns.set(rc = {'figure.figsize':(10, 6)})
sns.heatmap(correlation, annot=True)
plt.title("Correlation Matrix HeatMap")
plt.show()


# Linear Regression Analysis
lr_model = LinearRegression()
plot_model_pred("Linear Regression", 0, lr_model)

# KNN Classifier
knn_model = KNeighborsClassifier(n_neighbors=3)
plot_model_pred("KNN Classifier", 1, knn_model)

# Naive Bayes Algorithm: Gaussian
gaussian_model = GaussianNB()
plot_model_pred("Naive Bayes Gaussian", 1, gaussian_model)

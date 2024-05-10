"""
Program 7
-------------------------------------------------------------------------------------------------------
1. Generate 100000 rows, synthesized faculty dataset where experience linearly mapped to designation, 
    salary, no. of publications, no. of book chapters, amount of consultancy work, fund received, professional membership.
2. Read and load it into a list using function (try all the types of functions)
3. Find out the correlation among the fields in faculty dataset.
4. Perform the Linear regression analysis and plot the predicted value.
"""

import csv, random, math, os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd
from tqdm import tqdm
import seaborn as sns


def get_synthetic_faculty_dataset(num: int, filename: str) -> list:
    if filename in os.listdir(os.getcwd()):
        print(f"Found existing file and importing data....")
        with open(f"{filename}") as f:
            read = csv.reader(f)
            data = list(read)

            return data
    else:
        print("Creating new dataset...")
        data = []

        for i in tqdm(range(num)):
            experience = random.randint(1, 40)

            if experience < 7:
                designation = 1     # Associate Professor
            elif experience < 25:
                designation = 2     # Associate Professor
            else:
                designation = 3     # Professor

            salary = math.floor(random.randint(20000, 75000) * experience / designation)
            num_pubs = math.floor(random.randint(1, 10) * experience / designation)
            num_chapters = math.floor(random.randint(1, 100) * experience / designation)
            amt_consultancy_work = math.floor(random.randint(50000, 200000) * experience / designation)
            fund_received = math.floor(random.randint(50000, 1000000) * experience / designation)
            professional_membership = random.randint(1, 15)

            data.append([designation, experience, salary, num_pubs, num_chapters, amt_consultancy_work, fund_received, professional_membership])

        with open(f"{filename}", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Designation", "Experience", "Salary", "No. of Publications", "No. of Chapters", "Amount of consultancy work", "Fund Received", "Professional Membership"])
            writer.writerows(data)

        return data


dataset_file = "synthetic_data_faculty_for_linear_regression.csv"

data = get_synthetic_faculty_dataset(100000, dataset_file)

df = pd.read_csv(dataset_file)
correlation = df.corr()

sns.set(rc = {'figure.figsize':(10,6)})
sns.heatmap(correlation, annot=True)
plt.title("Correlation Heatmap Faculty Dataset")
plt.show()

X = df[["Experience"]]
Y = df["Salary"]

xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.2, random_state=99)
model = LinearRegression()
model.fit(xTrain, yTrain)

plt.scatter(xTest, yTest, color='black')
plt.plot(xTest, model.predict(xTest), color='red', linewidth=3)
plt.xlabel('Experience')
plt.ylabel('Salary')
plt.title('Linear Regression Analysis: Experience vs Salary')
plt.show()


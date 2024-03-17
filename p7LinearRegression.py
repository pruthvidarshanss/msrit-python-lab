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
print(f"\nData Correlation:\n")
print(correlation)

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


"""
Output:

Data Correlation:

                            Designation  Experience    Salary  No. of Publications  No. of Chapters  Amount of consultancy work  Fund Received  Professional Membership
Designation                    1.000000    0.912824  0.562339             0.434499         0.408594                    0.552792       0.431305                 0.000353
Experience                     0.912824    1.000000  0.687868             0.532954         0.502336                    0.676430       0.530115                -0.001661
Salary                         0.562339    0.687868  1.000000             0.420076         0.398403                    0.530734       0.423278                -0.005320
No. of Publications            0.434499    0.532954  0.420076             1.000000         0.310216                    0.414848       0.329431                -0.004747
No. of Chapters                0.408594    0.502336  0.398403             0.310216         1.000000                    0.390389       0.310512                -0.002202
Amount of consultancy work     0.552792    0.676430  0.530734             0.414848         0.390389                    1.000000       0.412340                -0.001321
Fund Received                  0.431305    0.530115  0.423278             0.329431         0.310512                    0.412340       1.000000                -0.002413
Professional Membership        0.000353   -0.001661 -0.005320            -0.004747        -0.002202                   -0.001321      -0.002413                 1.000000

"""
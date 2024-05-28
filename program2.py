"""
Program 2
--------------------------------------------------------------------------------------------------------------------------------------------
Write a Python program to do the following.
a. Create synthetic dataset for student details over 100000 rows with student name, USN, CGPA, address, blood group, 
    branch name, UG/PG, date of birth and year of studying. 
b. Then load dataset to tuple. 
c. Display menu for searching a student data. 
d. Read the branch name from the user and fetch the UG/PG students for where CGPA > 9.(So they can apply for placement)
"""


from faker import Faker
from tqdm import tqdm
import os, csv, random


def read_to_tuple(filename: str) -> tuple:
    with open(filename, "r") as f:
        read = csv.reader(f)
        data = [tuple(r) for r in read]
        data = tuple(data)
        
        return data


def generate_student(filename: str, num_records: int):
    fake = Faker()

    blood_group = ["O-", "O+", "AB+", "AB-", "B+", "B-"]
    ug_branches = ["CSE", "ME", "IS", "DS", "AI", "CIV", "EC"]
    pg_branches = ["CS", "CN", "IS", "DS", "RA"]

    data = []

    for i in tqdm(range(num_records)):
        name = fake.name()
        address = fake.address().replace("\n", ",")
        bg = random.choice(blood_group)
        degree = random.choice(["UG", "PG"])
        if degree == "UG":
            branch = random.choice(ug_branches) 
            dob = fake.date_of_birth(minimum_age=18, maximum_age=21)
            yos = random.randint(1, 4)
        else:
            branch = random.choice(pg_branches)
            dob = fake.date_of_birth(minimum_age=21, maximum_age=24)
            yos = random.randint(1, 2)
        
        cgpa = round(random.uniform(6.0, 10.0), 2)
        usn = f"1MS{24-yos}{degree}{branch}{fake.random_int(min=1, max=10000)}"

        data.append([name, usn, cgpa, address, bg, branch, degree, dob, yos])
    
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "USN", "CGPA", "Address", "BloodGroup", "Branch", "Program", "DateOfBirth", "YearOfStudying"])
        writer.writerows(data)

    tdata = read_to_tuple(filename)

    return tdata


data = generate_student("p2student.csv", 100000)

while True:
    try:
        print("Student Menu")
        print("-"*100)
        
        choice = input("1. Enter branch name for student data:\t")

        if choice == "1":
            branch = input("Enter branch name:\t")
            for i in data:
                if branch in i[5] and float(i[2]) >= 9:
                    print(f"Name:\t{i[0]}")
                    print(f"USN:\t{i[1]}")
                    print(f"CGPA:\t{i[2]}")
                    print(f"Branch:\t{i[5]}")
                    print(f"Program:\t{i[6]}")
                    print("\n\n")

        else:
            print("Invalid choice")
    
    except KeyboardInterrupt:
        exit()
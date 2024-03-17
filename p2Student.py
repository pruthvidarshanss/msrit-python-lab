"""
Program 2
------------------------------------------------------------------------------------------------------
Create synthetic dataset for student details over 100000 rows with student name, USN, CGPA, address, 
blood group, branch name, UG/PG, date of birth and year of studying.
Then load dataset to tuple. 
Display menu for search.
Dislpay the UG/PG students for a particular branch get the input from the user, where CGPA > 9.
"""

import csv

def read_csv(file: str) -> list:
    with open(file, newline="") as f:
        read = csv.reader(f)
        data = [tuple(row) for row in read]

        return data


def display_stud(data: tuple) -> None:
    print("-"*100)
    print(f"USN:\t{data[0]}")
    print(f"Name:\t{data[1]}")
    print(f"CGPA:\t{data[2]}")
    print(f"Address:\t{data[3]}")
    print(f"Blood Group:\t{data[4]}")
    print(f"Program:\t{data[5]}")
    print(f"Branch:\t{data[6]}")
    print(f"Date of Birth:\t{data[7]}")
    print(f"Year of studying:\t{data[8]}")
    print("-"*100)

studData = read_csv("synthetic_data_students.csv")

while True:
    try:
        print("-" * 100)
        print("Student Database Menu")
        print("-" * 100)
        print("1. Display student details for a particular branch of UG/PG with CGPA more than 9")
        print("Enter any other key to exit\n")

        choice = input("Enter your choice:\t")

        if choice == "1":
            f = False
            name = input("\nEnter student name:\t")
            program = input("Is the student belongs to UG/PG program?\t").upper()
            for i in range(len(studData)):
                if name in studData[i][1] and program in studData[i][5] and float(studData[i][2]) > 9.0:
                    display_stud(studData[i])
                    f = True

            if not f:
                print(f"{name} not found!\n")

        else:
            print("\nExiting....!")
            exit()

    except KeyboardInterrupt:
        print("\nExiting....!")
        exit()
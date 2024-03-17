"""
PROGRAM 1
------------------------------------------------------------------------------------------------------------------
Create over 100000 data to a CSV file. Read it to list. Use menu operators to add, search, delete from the list.
Read experience(number) from user & display the faculty name, so that they can participate in BOS.
"""

import csv

def update_csv(filename: str, data: list) -> None:
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def read_csv(file: str) -> list:
    with open(file, newline="") as f:
        read = csv.reader(f)
        data = list(read)

        return data


def display_faculty(info: list) -> None:
    print("-" * 100)
    print(f"Faculty Name:\t{info[1]}")
    print(f"Faculty Experience:\t{info[2]}")
    print(f"Faculty Designation:\t{info[3]}")
    print(f"Faculty Salary:\t{info[4]}")
    print(f"Number of publications from faculty:\t{info[5]}")
    print("-" * 100)


data = read_csv("synthetic_data_faculty.csv")

while True:
    try:
        print("-" * 100)
        print("Faculty Database Menu")
        print("-" * 100)
        print("1. Add new faculty details to the database")
        print("2. Enter faculty name to search from the database")
        print("3. Delete a faculty details from the database")
        print("4. Enter experience number to display faculty details")
        print("\nEnter any other key to exit")

        choice = input("Enter your choice:\t")

        if choice == "1":
            fID = int(data[-1][0]) + 1
            fName = input("Enter faculty name:\t")
            exp = int(input("Enter faculty experience:\t"))
            design = input("Enter faculty designation:\t")
            salary = int(input("Enter faculty salary:\t"))
            npub = int(input("Enter number of publications:\t"))

            data.append([fID, fName, exp, design, salary, npub])
            print("Data inserted successfully:")
            print(f"Faculty Name:\t{fName}")
            print(f"Faculty Experience:\t{exp}")
            print(f"Faculty Designation:\t{design}")
            print(f"Faculty Salary:\t{salary}")
            print(f"Number of publications from faculty:\t{npub}")

            update_csv("synthetic_data_faculty.csv", data)

        elif choice == "2":
            f = False
            fsearch = input("Enter faculty name:\t")
            for i in range(len(data)):
                try:
                    if fsearch in data[i][1]:
                        display_faculty(data[i][:])
                        f = True
                except IndexError:
                    pass

            if not f:
                print(f"{fsearch} not found!")

        elif choice == "3":
            f = False
            fsearch = input("Enter faculty name to delete from the database:\t")
            for i in range(len(data)):
                try:
                    if fsearch in data[i][1]:
                        display_faculty(data[i][:])
                        data.remove(data[i][:])
                        f = True
                except IndexError:
                    pass
            if not f:
                print(f"{fsearch} not found!")

            update_csv("synthetic_data_faculty.csv", data)

        elif choice == "4":
            f = False
            fsearch = input("Enter experience:\t")
            for i in range(len(data)):
                try:
                    if fsearch in data[i][2]:
                        display_faculty(data[i][:])
                        f = True
                except IndexError:
                    pass
            if not f:
                print(f"We cannot find faculties publications more than {fsearch}!")

        else:
            print("\nExiting....!")
            exit()

    except KeyboardInterrupt:
        print("\nExiting....!")
        exit()

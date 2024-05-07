"""
Program 1
--------------------------------------------------------------------------------------------------------------------------------------------
Write a Python program to do the following.
a. Create synthetic faculty data set with 100000 rows in a CSV file. 
b. Load it to list in python. 
c. Use menu operators to add, search, delete from the list. 
d. Read experience of faculty (number) from user & display the faculty name, if it is > 10 years display that they can participate in BOS.
"""

from faker import Faker
import os, random, csv
from tqdm import tqdm


def save_to_csv(filename: str, data: list) -> None:
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["FacultyID", "Name", "Experience"])
        writer.writerows(data)


def generate_faculty_dataset(filename: str, num_records: int) -> list:
    fake = Faker()
    data = []

    for i in tqdm(range(num_records)):
        name = fake.name()
        exp = random.randint(2, 12)
        
        data.append([i+1, name, exp])
    
    save_to_csv(filename, data)

    return data

dataset = "faculty_data.csv"

fdata = generate_faculty_dataset(dataset, 100000)

while True:
    try:    
        print("Faculty Database:")
        print("-"*100)
        print("Choose any one option to continue")

        choice = input("1. To add faculty data\n2. To search faculty data\n3. To delete faculty data\n4. Enter experience to display faculty names\n\n")

        if choice == "1":
            name = input("Enter faculty name:\n")
            exp = int(input("Enter faculty experience:\n"))

            print(f"Faculty Details Inserted successfully:\n\tName: {name}\t Experience: {exp}\n")

            fdata.append([fdata[-1][0]+1, name, exp])
            save_to_csv(dataset, fdata)
            

        elif choice == "2":
            name = input("Enter faculty name:\n")

            for d in fdata:
                if name in d[1]:
                    print(f"Faculty Details Found:\n\tName: {d[1]}\t Experience: {d[2]}\n")


        elif choice == "3":
            name = input("Enter faculty name:\n")

            f = False
            for d in fdata:
                if name in d[1]:
                    fdata.remove(d)
                    print(f"Faculty Details Deleted\n\tName: {d[1]}\t Experience: {d[2]}\n")
                    f = True
            
            if not f:
                print(f"Cannot find faculty details form teh name: {name}")
            else:
                save_to_csv(dataset, fdata)
            
        elif choice == "4":
            exp = int(input("Enter faculty experience:\n"))

            f = False
            for d in fdata:
                if exp > 10 and int(d[2]) > 10:
                    print(f"This faculty is qualified to participate in BOS...\t Name: {d[1]}\t Experience: {d[2]}")
                    f = True
            
            if not f:
                print("None of the faculty can participate in BOS...!\n")

            print()
        
        else:
            print("Invalid choice...!")

    except Exception as e:
        print(f"Error: {e}")
        pass

    except KeyboardInterrupt:
        print("Exiting....!")
        exit()
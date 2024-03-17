import csv
from faker import Faker
import random
from tqdm import tqdm

def generate_synthetic_data(num_records: int) -> list:
    fake = Faker()
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    programs = ['UG', 'PG']
    ug_branch = ['CSE', "ISE", "AIDS", "AIML", "ECE", "ME", "CIV", "EE"]
    pg_branch = ["CSE", "CNE", "RAI", "BT", "AIML", "DS"]
    
    data = []
    for _ in tqdm(range(num_records)):
        student_name = fake.name()
        cgpa = round(random.uniform(6.0, 10.0), 2)
        address = fake.address().replace("\n", ",")
        blood_group = random.choice(blood_groups)
        program = random.choice(programs)
        branch_name = random.choice(ug_branch) if program == 'UG' else random.choice(pg_branch)
        dob = fake.date_of_birth(minimum_age=17, maximum_age=25).strftime('%d-%m-%Y')
        year_of_studying = random.randint(1, 4) if program == "UG" else random.randint(1, 2)
        usn = f"1MS{24-year_of_studying}{branch_name}{program}{fake.random_int(min=1, max=10000)}"
        
        data.append([usn, student_name, cgpa, address, blood_group, program, branch_name, dob, year_of_studying])

    return data

def save_to_csv(filename: str, data: list) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['USN', 'Student Name', 'CGPA', 'Address', 'Blood Group', 'UG/PG', 'Branch Name', 'Date of Birth', 'Year of Studying'])
        writer.writerows(data)

# Generate synthetic data
num_records = 100000  # Change this value to generate different number of records
synthetic_data = generate_synthetic_data(num_records)

# Save data to CSV file
save_to_csv('synthetic_data_students.csv', synthetic_data)

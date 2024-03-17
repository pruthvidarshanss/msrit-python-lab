import csv
from faker import Faker
import random
from tqdm import tqdm

def generate_synthetic_data(num_records: int) -> list:
    fake = Faker()
    designations = ['Professor', 'Associate Professor', 'Assistant Professor']
    
    data = []
    for i in tqdm(range(num_records)):
        faculty_name = fake.name()
        experience = random.randint(1, 30)  # Experience in years
        designation = random.choice(designations)
        salary = random.randint(50000, 150000)  # Salary range
        num_publications = random.randint(0, 100)  # Number of publications
        
        data.append([i+1, faculty_name, experience, designation, salary, num_publications])
    
    return data

def save_to_csv(filename: str, data: list) -> None:
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Faculty ID', 'Faculty Name', 'Experience (years)', 'Designation', 'Salary ($)', 'Publications'])
        writer.writerows(data)

# Generate synthetic data
num_records = 100000  # Change this value to generate different number of records
synthetic_data = generate_synthetic_data(num_records)

# Save data to CSV file
save_to_csv('synthetic_data_faculty.csv', synthetic_data)

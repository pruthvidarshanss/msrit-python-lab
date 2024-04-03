# `Realtime Application Development Using Python`

## [`Program 1`](p1Faculty.py)

Create over 100000 data to a CSV file. Read it to list. Use menu operators to add, search, delete from the list.
Read experience(number) from user & display the faculty name, so that they can participate in BOS.

## [`Program 2`](p2Student.py)

Create synthetic dataset for student details over 100000 rows with student name, USN, CGPA, address, 
blood group, branch name, UG/PG, date of birth and year of studying. Then load dataset to tuple. Display menu for search. Dislpay the UG/PG students for a particular branch get the input from the user, where CGPA > 9.

## [`Program 3`](p3Weather.py)

Weather details displaying for a particular place given longitude & latitude in the globe. Read longitude & latitude values from the user and store weather details to a dictionary.

## [`Program 4`](p4Blink.py)

Write a Python program demonstrate continous blinking of a LED (blinking effect) using Raspberry PI and RPi.GPIO library

## [`Program 5`](p5SingleSequence.py)

Write a Python program demonstrate single sequence of turning ON the LED for one second and then turning it OFF.

## [`Program 6`](P6LDR.py)

Write a Python program to detect the intensity of light in surrounding using a LDR(Light Dependent Resistor) and display the LDR Value as output.

## [`Program 7`](p7LinearRegression.py)

1. Generate 100000 rows, synthesized faculty dataset where experience linearly mapped to designation, salary, no. of publications, no. of book chapters, amount of consultancy work, fund received, professional membership.
2. Read and load it into a list using function (try all the types of functions)
3. Find out the correlation among the fields in faculty dataset.
4. Perform the Linear regression analysis and plot the predicted value.

## [`Program 8`](p8MLFaculty.py)

Generate 100000 rows and put in csv file, sythesized faculty dataset where experience linearly mapped to designation,
salary, no. of publications, no. of chapters, amount of consultancy work, fund recieved, professional membership.

1. Read csv file and load it into tuple Tuple and Dictionary using Function, (try all the types of function)
2. Find out correlation among the fields in faculty dataset
3. Perform the following operations:
    1. Linear Regression analysis of following & plot the predicted value in separate graphs
    2. KNN analysis of following & plot the predicted value in separate graphs
    3. Apply Naiye Bayes algorithm for following & plot the predicted value in separate graphs (x-axis - experience, y-axis - predicted value)
         1. No. of publication
         2. No. of Book chapters
         3. AMount of Consultancy work
         4. Fund Received
         5. Professional Membership


## [`Program 9`](p9FacultyAssociationRules.py)

Generate 1,00000 rows and put in csv file, synthesized data faculty data set where experience linearly mapped to designation, 
salary, no of publication, no of book chapters, amount of consultancy work, fund received, professional membership.
1. Read csv file and load it into tuples (try lambda function)
2. Perform the following operations:
    1. Using regular expression search for associate professors with more than 15 years experience, assistant Professors with more than 5 years experience, Professors with more than 20 years experience
    2. Analyze the association rule mining of associate professors for their following performance relations in different contributions
        1. No. of publication and no of book chapters
        2. No. of publication and amount of consultancy work
        3. No. of publication and fund received
        4. No. of publication and professional membership


## [`Program 10`](p10FacultyClassAndObjects.py)

Generate 100000 rows and put it in csv file, synthesized data faculty dataset where experience linearly mapped to designation,
salary, no. of publications, no. of chapters, amount of consultancy work, fund received and professional membership
1. Use classes and objects for the following operations:
    1. Read csv file and load it into temp variables
    2. Perform the following operations
        1. Using lambda and regular expression to search for associate professors with more than 25 years experience and 
            load in another temp list called "asso_prof_25"
        2. In asso_prof_25 list do the following factoring:
            1. If experience > 25, yes means set the value as 1 else 0
            2. If publication count > 5, yes means set the value as 1 else 0
            3. Similarly do for no. of publications > 3, amount of consultancy work > 50000, fund received > 500000, 
                professional membership > 2
        3. Analyze the association rule mining of associate professors for the following performance relations in different contributions
            1. Exerience, designation, no. of publications and no. of book chapters
            2. Exerience, designation, no. of publications and amount of consultancy work
            3. Exerience, designation, no. of publications and fund received
            3. Exerience, designation, no. of publications and professional membership
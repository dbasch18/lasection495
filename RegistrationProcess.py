import pandas as pd
import re
import random
from datetime import datetime, timedelta

# Use the correct path to the CSV file
csv_file_path = '/Users/jayedahmed/Downloads/MOCK_DATA.csv'

# Load the user database from CSV
user_data = pd.read_csv(csv_file_path)


# Function to validate phone number format
def validate_phone_number(phone_number):
    return bool(re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number))


# Function to generate a 6-digit verification code
def generate_verification_code():
    return random.randint(100000, 999999)


# Simulated function to send the verification code via email
def send_verification_email(receiver_email, verification_code):
    # In this simulated example, we'll print the code to the console
    print(f"Simulated: Verification code {verification_code} sent to {receiver_email}. It expires in 5 minutes.")


# Function to register a user
def register_user():
    global user_data  # Declare this at the top before accessing user_data

    # Gather user input for first and last name
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")

    # Loop to keep asking for email until a unique one is provided
    while True:
        email = input("Enter Email: ")
        if email in user_data['email'].values:
            print("This email is already in use. Please enter a different email.")
        else:
            break

    # Loop to keep asking for phone number until a unique one is provided and format is correct
    while True:
        phone_number = input("Enter Phone Number (###-###-####): ")
        if not validate_phone_number(phone_number):
            print("Invalid phone number format. Please enter as ###-###-####.")
        elif phone_number in user_data['phoneNumber'].values:
            print("This phone number is already in use. Please enter a different phone number.")
        else:
            break

    # Ask if the user is registering as an employee or customer
    user_type = input("Are you registering as an 'employee' or 'customer'?: ").lower()

    employee_location = None  # Initialize employee location
    # Check for employee registration and validate code
    if user_type == "employee":
        while True:
            employee_code = input("Enter employee code for your location: ").upper()
            if employee_code == "ABC":
                employee_location = "CDN"
                break
            elif employee_code == "123":
                employee_location = "EXO"
                break
            else:
                print("Invalid employee code.")

    # Generate and send a verification code via email
    verification_code = generate_verification_code()
    send_verification_email(email, verification_code)

    # Record the time the verification code was generated
    code_expiration_time = datetime.now() + timedelta(minutes=5)

    # Prompt user to enter the verification code
    user_code = input("Enter the verification code: ")

    # Check if the code is valid and not expired
    if int(user_code) == verification_code and datetime.now() < code_expiration_time:
        # Generate a new user ID
        new_user_id = user_data['userID'].max() + 1

        # Register as employee or customer
        if user_type == "employee":
            new_user = pd.DataFrame([{
                'userID': new_user_id,
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'phoneNumber': phone_number,
                'userType': f"Employee - {employee_location}"
            }])
            print(f"Thank you for registering as a {employee_location} employee!")
        else:
            new_user = pd.DataFrame([{
                'userID': new_user_id,
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'phoneNumber': phone_number,
                'userType': "Customer"
            }])
            print("Thank you for registering as a customer!")

        # Append the new user to the DataFrame using pd.concat()
        user_data = pd.concat([user_data, new_user], ignore_index=True)

        # Save the updated DataFrame back to CSV
        user_data.to_csv(csv_file_path, index=False)

        print(f"User {first_name} {last_name} has been successfully registered!")
    else:
        print("Invalid verification code or code expired.")


# Call the register_user function to start the process
register_user()
import os
import time
import hashlib
import collections
from pymongo import MongoClient

# Function to hash a CPF number using SHA-256
def hash_cpf(cpf):
    """Hashes the CPF info using SHA-256 and returns the hash."""
    # Encode the cpf to bytes, required for hashing
    result = hashlib.sha256(cpf.encode()).hexdigest()
    return result

# Function to clear the terminal screen
def clear():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')  # Clear the console on Windows
    else:
        os.system('clear')  # Clear the console on Unix/Linux/Mac

# Main function to execute the program
def main():
    # Connect to the MongoDB server on the default port
    client = MongoClient("mongodb://mongo:27017/")
    
    # Access the 'users' database
    db = client.users
    
    # Access the 'user_data' collection within the 'users' database
    users_collection = db.user_data
    
    # Notify user on how to exit
    print('Type \'exit\' to leave the program')

    # Infinite loop to continuously accept user input
    while True:
        # Information categories to collect
        info = ['name', 'age', 'cpf']
        # namedtuple for structured data storage
        User = collections.namedtuple('User', info)
        # List to hold the user's data
        data = []

        # Iterate over each information category to collect input
        for collected_info in info:
            prompt = input(f'What is your {collected_info}: ')
            
            # Break the loop if the user types 'exit'
            if prompt == 'exit':
                break 
            else:
                # Append the data to the list; hash the cpf value
                if collected_info == 'cpf':
                    data.append(hash_cpf(prompt))
                else:
                    data.append(prompt)
        
        # Create a User namedtuple if data was provided
        user = User(*data) if any(data) else None

        # Check if the user was created
        if user is None:
            print("Exiting the program...")
            break
        
        # Insert the user data into MongoDB and print the ID of the inserted document
        result = users_collection.insert_one(user._asdict())
        print("User saved successfully! ID:", result.inserted_id)
        # Pause for 0.3 seconds before clearing the screen
        time.sleep(.3)
        clear()


if __name__ == "__main__":
    main()

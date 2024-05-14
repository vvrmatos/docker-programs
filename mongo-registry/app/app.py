import os
import time
import hashlib
import collections
from pymongo import MongoClient

def hash_cpf(cpf):
    """Hashes the CPF info using SHA-256 and returns the hash."""
    result = hashlib.sha256(cpf.encode()).hexdigest()
    return result

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def main():
    client = MongoClient("mongodb://mongo:27017/")
    
    db = client.users
    
    users_collection = db.user_data
    
    print('Type \'exit\' to leave the program')

    while True:
        info = ['name', 'age', 'cpf']
        User = collections.namedtuple('User', info)
        data = []

        for collected_info in info:
            prompt = input(f'What is your {collected_info}: ')
            
            if prompt == 'exit':
                break 
            else:
                data.append(prompt) if collected_info != 'cpf' else data.append(hash_cpf(collected_info))
        
        user = User(*data) if any(data) else None

        if user is None:
            print("Exiting the program...")
            break
        
        result = users_collection.insert_one(user._asdict())
        print("User saved successfully! ID:", result.inserted_id)
        time.sleep(.3)
        clear()


if __name__ == "__main__":
    main()

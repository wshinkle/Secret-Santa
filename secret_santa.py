from smtp2go.core import Smtp2goClient
import random
from dotenv import load_dotenv
import os
import copy


def randomize(people: list)-> list:
    people_copy = copy.deepcopy(people)
    final = []
    while len(people) > 0:
        if len(people) == 1:
            print("Only one person left--Reassigning")
            people = copy.deepcopy(people_copy)
            final = []
            continue
        
        santa = random.choice(people)
        if santa[2] == 0:
            recipient = random.choice(people)
            if santa[0] == recipient[0]:
                continue
            if recipient[3] == 0:
                santa[2] = 1
                recipient[3] = 1
                if santa[2] == 1 and santa[3] == 1:
                    people.remove(santa)
                if recipient[2] == 1 and recipient[3] == 1:
                    people.remove(recipient)
                
                
                final.append({"santa": {'name': santa[0], 'email': santa[1]}, "recipient": recipient[0]})

    return final




if __name__ == '__main__':
    # List of people to send to
    load_dotenv()
    email_client = Smtp2goClient(api_key=os.getenv('API_KEY'))
    sender = os.getenv('SENDER')
    
    raw_people = []
    with open('participants.txt') as f:
        raw_people = f.readlines()
    
    people = []
    for person in raw_people:
        temp = person.split(',')
        people.append([temp[0], temp[1].strip(), 0, 0])

    print("List of people: ")
    for person in people:
        print(person[0])
    print("\n\n")
    sending_list = randomize(people)
    for pair in sending_list:
        payload = {
            'sender': sender,
            'recipients': [pair['santa']['email']],
            'subject': 'Secret Santa',
            'text': 'Information about your recipient',
            'html': f'<html><body><h1>Your recipient is {pair["recipient"]} </h1></body><html>',
        }
        response = email_client.send(**payload)
        print(f'Email sent to {pair["santa"]["name"]} at {pair["santa"]["email"]}: {response.success}')
        print("\n\n")

               
"""
conference_call.py

A simple script that can be used to start a conference call, and
ends the conference by sending a text message to all members of the conference.

This script uses Bandwidth's Messaging V2 API and Bandwidth's Voice API, and accesses
these APIs directly using the Python request library.

Author: Jacob Mulford

Copywrite Bandwidth INC 2018
"""

import requests


usage = """
python conference_call.py <member-1-number> <member-2-number> ... <member-n-number> <bandwidth_phone_number>

Phone numbers must be in +1XXXYYYZZZZ format

There is a limit of 10 member numbers for sending a group text, and you must have at least 3 numbers to make a conference call.
The <bandwidth_phone_number> is your Bandwidth phone number that will start the conference call and send the ending group text.
"""


try:
    import os
    BANDWIDTH_USER_ID = os.environ['BANDWIDTH_USER_ID']
    BANDWIDTH_API_TOKEN = os.environ['BANDWIDTH_API_TOKEN']
    BANDWIDTH_API_SECRET = os.environ['BANDWIDTH_API_SECRET']
    AUTH = (BANDWIDTH_API_TOKEN, BANDWIDTH_API_SECRET)
except:
    print("You need to set the following environmental variables: BANDWIDTH_USER_ID, BANDWIDTH_API_TOKEN, BANDWIDTH_API_SECRET")
    exit(-1)


def end_conference_with_text(conference_id, phone_numbers, bandwidth_phone_number):
    """
    Ends the conference call with a text message send with the user's input

    Args:
        conference_id (str): ID of the conference to end
        phone_numbers (list<str>): All phone numbers in the conference
        bandwidth_phone_number (str): The Bandwidth phone number used to send the conference ending group text

    Returns:
        void
    """
    #Waits for the creator to put in input for the ending text message
    group_text_message = input("Please type your ending text message and press enter when you are ready to end conference " + conference_id + ":\n")

    #End the conference
    end_conference_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences/{conference_id}".format(user_id = BANDWIDTH_USER_ID, conference_id = conference_id)
    end_conference_payload = {
        "state": "completed"
    }
    requests.post(end_conference_url, auth=AUTH, json=end_conference_payload)

    #Send the text message to all members of the conference
    ##TODO: Change to V2 group message
    ##TODO: Change to pull members from conference and get their phone numbers from the associated call
    send_text_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/messages".format(user_id = BANDWIDTH_USER_ID)
    send_text_payload = {
        "from": bandwidth_phone_number,
        "to": "",
        "text": group_text_message
    }
    for phone_number in phone_numbers:
        send_text_payload["to"] = phone_number
        requests.post(send_text_url, auth=AUTH, json=send_text_payload)

    print("Conference " + conference_id + " has been ended. Group text send by " + bandwidth_phone_number)
    print("Group text message: " + group_text_message)


def start_conference(phone_numbers, bandwidth_phone_number):
    """
    Starts the conference call

    Args:
        phone_numbers (list<str>): The phone numbers to be added to the conference
        bandwidth_phone_number: The Bandwidth phone number used to start the conference

    Returns:
        str: The ID of the conference call
    """
    #Start the conference
    conference_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences".format(user_id = BANDWIDTH_USER_ID)
    start_conference_payload = {
        "from": bandwidth_phone_number
    }
    response = requests.post(conference_url, auth=AUTH, json=start_conference_payload)

    #Get the conference id. The response Location value looks like this:
    #https://api.catapult.inetwork.com/v1/users/{userId}/conferences/{conferenceId}
    conference_id = response.headers['Location'].split("/")[-1]

    #Create the calls and add them to the conference. The "conferenceId" value must be set to the current conference id
    #when creating a call in order to allow the call to be added to the conference
    create_call_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/calls".format(user_id = BANDWIDTH_USER_ID)
    create_call_payload = {
        "from": bandwidth_phone_number,
        "to": "",
        "conferenceId": conference_id
    }
    add_call_to_conference_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences/{conference_id}/members".format(user_id = BANDWIDTH_USER_ID, conference_id = conference_id)
    add_call_to_conference_payload = {
        "callId": ""
    }

    for phone_number in phone_numbers:
        #Create call
        create_call_payload["to"] = phone_number
        response = requests.post(create_call_url, auth=AUTH, json=create_call_payload)

        #Get call id. This is needed to add the call to the conference. The response Location value looks like this:
        #https://api.catapult.inetwork.com/v1/users/{userId}/calls/{callId}
        call_id = response.headers['Location'].split("/")[-1]

        #Add call to conference
        add_call_to_conference_payload["callId"] = call_id
        response = requests.post(add_call_to_conference_url, auth=AUTH, json=add_call_to_conference_payload)

    print("Conference call has been started by " + bandwidth_phone_number + " to " + str(phone_numbers))
    return conference_id


def main(phone_numbers, bandwidth_phone_number):
    """
    Main method for the script

    Args:
        phone_numbers (list<string>): The phone numbers to use for the conference
        bandwidth_phone_number (str): The Bandwidth phone number to send the ending group text

    Returns:
        void
    """
    conference_id = start_conference(phone_numbers, bandwidth_phone_number)
    end_conference_with_text(conference_id, phone_numbers, bandwidth_phone_number)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 5 or len(sys.argv) > 12:
        print("You must have at least 3 phone numbers to make a conference call. The maximum number of phone numbers allowed is 10")
        print(usage)
        exit(-1)

    main(sys.argv[1:-1], sys.argv[-1])

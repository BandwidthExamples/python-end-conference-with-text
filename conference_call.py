"""
conference_call.py

A simple script that launches a server that can be used to start a conference call, and
ends the conference by sending a text message to all members of the conference.

This script uses Bandwidth's Messaging API and Bandwidth's Voice API, and accesses
these APIs directly using the Python request library.

Author: Jacob Mulford

Copywrite Bandwidth INC 2018
"""

import requests
import json
from flask import Flask, request


try:
    import os
    BANDWIDTH_USER_ID = os.environ['BANDWIDTH_USER_ID']
    BANDWIDTH_API_TOKEN = os.environ['BANDWIDTH_API_TOKEN']
    BANDWIDTH_API_SECRET = os.environ['BANDWIDTH_API_SECRET']
    BANDWIDTH_PHONE_NUMBER = os.environ['BANDWIDTH_PHONE_NUMBER']
    USER_PHONE_NUMBER = os.environ['USER_PHONE_NUMBER']
    AUTH = (BANDWIDTH_API_TOKEN, BANDWIDTH_API_SECRET)
except:
    print("You need to set the following environmental variables: BANDWIDTH_USER_ID, BANDWIDTH_API_TOKEN, BANDWIDTH_API_SECRET, BANDWIDTH_PHONE_NUMBER, USER_PHONE_NUMBER")
    exit(-1)

CONFERENCE_ID = None
app = Flask(__name__)


def end_conference_with_text(group_text_message):
    """
    Ends the conference call with a text message sent with the user's input

    Args:
        group_text_message (str): The message sent after the conference is ended

    Returns:
        void
    """
    #End the conference
    end_conference_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences/{conference_id}".format(user_id = BANDWIDTH_USER_ID, conference_id = CONFERENCE_ID)
    end_conference_payload = {
        "state": "completed"
    }
    requests.post(end_conference_url, auth=AUTH, json=end_conference_payload)

    #Send the text message to all members of the conference
    #This is done in the following steps:
        #1: Build the url and payload for sending the text message
        #2: Pull all of the conference members from Bandwidth's API
        #3: For each conference member, grab the associated call information from Bandwidth's API
        #4: With the call information, grab the conference member's phone number based on the direction of the call
        #5: Send the text message
    send_text_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/messages".format(user_id = BANDWIDTH_USER_ID)
    send_text_payload = {
        "from": BANDWIDTH_PHONE_NUMBER,
        "to": "",
        "text": group_text_message
    }

    get_conference_members_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences/{conference_id}/members".format(user_id = BANDWIDTH_USER_ID, conference_id = CONFERENCE_ID)
    #This endpoint returns a list of conference members as JSON
    conference_members = json.loads(requests.get(get_conference_members_url, auth=AUTH).text)
    conference_members_phone_numbers = []

    for conference_member in conference_members:
        #Each conference member is a JSON dictionary that looks like this
        """
        {
            'addedTime': '{time}',
            'call': 'https://api.catapult.inetwork.com/v1/users/{userId}/calls/{callId}',
            'hold': boolean,
            'id': '{memberId}',
            'mute': boolean,
            'state': 'string',
            'joinTone': boolean,
            'leavingTone': boolean
        }
        """

        #The url in the 'call' field can be used to get information on this member's call
        get_call_information_url = conference_member["call"]

        #Call information is a JSON dictionary that looks like this
        """
        {
            'activeTime': '{time}',
            'chargeableDuration': int,
            'conference': 'https://api.catapult.inetwork.com/v1/users/{userId}/conferences/{conferenceId}',
            'direction': 'out',
            'endTime': '{time}',
            'events': 'https://api.catapult.inetwork.com/v1/users/{userId}/calls/{callId}/events',
            'from': '+1XXXYYYZZZZ',
            'id': '{callId}',
            'recordingFileFormat': 'string',
            'recordingEnabled': boolean,
            'recordings': 'https://api.catapult.inetwork.com/v1/users/{userId}/calls/{callId}/recordings',
            'startTime': '{time}',
            'state': 'string',
            'to': '+1XXXYYYZZZZ',
            'transcriptionEnabled': boolean,
            'transcriptions': 'https://api.catapult.inetwork.com/v1/users/{userId}/calls/{callId}/transcriptions'
        }
        """
        call_information = json.loads(requests.get(get_call_information_url, auth=AUTH).text)

        #"direction" is "out" for a call that was originated by Bandwidth, and "from" will be the Bandwidth number and "to"
        #will be the conference member's number. If "direction" is "in", these values are swapped.
        #This allows us to get phone numbers from people who called into the conference and were called into the conference,
        #and ignores those who declined to join the conference.
        call_direction = call_information["direction"]
        if call_direction == "out":
            phone_number = call_information["to"]
        else:
            phone_number = call_information["from"]
        
        #Sends the text message to the phone number
        send_text_payload["to"] = phone_number
        requests.post(send_text_url, auth=AUTH, json=send_text_payload)
        conference_members_phone_numbers.append(phone_number)

    #Notify the one who started the conference of everyone who attended
    send_text_payload["to"] = USER_PHONE_NUMBER
    send_text_payload["text"] = "Conference attendees: " + str(conference_members_phone_numbers)
    requests.post(send_text_url, auth=AUTH, json=send_text_payload)


def start_conference(phone_numbers):
    """
    Starts the conference call

    Args:
        phone_numbers (list<str>): The phone numbers to be added to the conference

    Returns:
        str: The ID of the conference call
    """
    #Start the conference
    conference_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences".format(user_id = BANDWIDTH_USER_ID)
    start_conference_payload = {
        "from": BANDWIDTH_PHONE_NUMBER
    }
    response = requests.post(conference_url, auth=AUTH, json=start_conference_payload)

    text_message = "You have been invited by {user_phone} to join a conference call on {bandwidth_phone}. Please call this number to join.".format(user_phone = USER_PHONE_NUMBER, bandwidth_phone = BANDWIDTH_PHONE_NUMBER)

    #Send each number an invite to the conference
    send_text_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/messages".format(user_id = BANDWIDTH_USER_ID)
    send_text_payload = {
        "from": BANDWIDTH_PHONE_NUMBER,
        "to": "",
        "text": text_message
    }

    for phone_number in phone_numbers:
        #Sends the text message to the phone number
        send_text_payload["to"] = phone_number
        requests.post(send_text_url, auth=AUTH, json=send_text_payload)

    #Notify the starter of the conference that the conference has started
    send_text_payload["to"] = USER_PHONE_NUMBER
    send_text_payload["text"] = "You have started the conference! Please respond to this message when you are ready to end the conference. Your message will be forwarded to all conference participants."
    requests.post(send_text_url, auth=AUTH, json=send_text_payload)
    
    #Get the conference id. The response Location value looks like this:
    #https://api.catapult.inetwork.com/v1/users/{userId}/conferences/{conferenceId}
    conference_id = response.headers['Location'].split("/")[-1]

    return conference_id


def add_call_to_conference(call_id, conference_id):
    """
    Adds the call to the conference

    Args:
        call_id (str): The call id to add to the conference
        conference_id (str): The id of the conference

    Returns:
        void
    """
    add_call_to_conference_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/conferences/{conference_id}/members".format(user_id = BANDWIDTH_USER_ID, conference_id = conference_id)
    add_call_to_conference_payload = {
        "callId": call_id
    }

    requests.post(add_call_to_conference_url, auth=AUTH, json=add_call_to_conference_payload)


@app.route("/message", methods=["POST"])
def incoming_message_handler():
    global CONFERENCE_ID

    data = json.loads(request.data)
    incoming_number = data["from"]
    text_message = data["text"]

    if CONFERENCE_ID is None and incoming_number == USER_PHONE_NUMBER:
        phone_numbers = text_message.split(" ")
        if len(phone_numbers) > 20:
            send_text_url = "https://api.catapult.inetwork.com/v1/users/{user_id}/messages".format(user_id = BANDWIDTH_USER_ID)
            send_text_payload = {
                "from": BANDWIDTH_PHONE_NUMBER,
                "to": USER_PHONE_NUMBER,
                "text": "You cannot have more than 20 participants in a conference"
            }
            requests.post(send_text_url, auth=AUTH, json=send_text_payload)
            return ""

        CONFERENCE_ID = start_conference(phone_numbers)

    elif CONFERENCE_ID is not None and incoming_number == USER_PHONE_NUMBER:
        end_conference_with_text(text_message)
        CONFERENCE_ID = None

    return ""


@app.route("/voice", methods=["POST"])
def incoming_voice_handler():
    global CONFERENCE_ID

    data = json.loads(request.data)

    if CONFERENCE_ID is not None:
        call_id = data["callId"]
        add_call_to_conference(call_id, CONFERENCE_ID)

    return ""


if __name__ == '__main__':
    app.run()

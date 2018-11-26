"""
conference_call.py

A simple script that can be used to start a conference call, and
upon completion of the conference call sends a text message to all
members of the conference.

This script uses Bandwidth's Messaging V2 API and Bandwidth's Voice API, and accesses
these APIs directly (not through an SDK)

Author: Jacob Mulford

Copywrite Bandwidth INC 2018
"""


usage = """
python conference_call.py <member-1-number> <member-2-number> ... <member-n-number> <bandwidth_phone_number>

Phone numbers must be in +1XXXYYYZZZZ format

There is a limit of 10 member numbers for sending a group text, and you must have at least 3 numbers to make a conference call.
The <bandwidth_phone_number> is your Bandwidth phone number that will start the conference call and send the ending group text.
"""


try:
    import os
    BANDWIDTH_USER_ID = os.environ['BANDWIDTH_USER_ID']
    BANDWIDTH_API_SECRET = os.environ['BANDWIDTH_API_SECRET']
    BANDWIDTH_API_TOKEN = os.environ['BANDWIDTH_API_TOKEN']
except:
    print("You need to set the following environmental variables: BANDWIDTH_USER_ID, BANDWIDTH_API_SECRET, BANDWIDTH_API_TOKEN")
    exit(-1)


def end_conference_with_text(conference_id, bandwidth_phone_number):
    """
    Ends the conference call on user input

    Args:
        conference_id (str): ID of the conference to end
        bandwidth_phone_number (str): The Bandwidth phone number used to send the conference ending group text
    """
    group_text_message = input("Please type your ending text message and press enter when you are ready to end conference " + conference_id + ":\n")
    print("Conference " + conference_id + " has been ended. Group text send by " + bandwidth_phone_number)
    print("Group text message: " + group_text_message)


def start_conference(phone_numbers, bandwidth_phone_number):
    """
    Starts the conference call

    Args:
        phone_numbers (list<str>): The phone numbers to use for the conference
        bandwidth_phone_number: The Bandwidth phone number

    Returns:
        str: The ID of the conference call
    """
    print("Conference call has been started by " + bandwidth_phone_number + " to " + str(phone_numbers))
    return "34dladc3"


def main(phone_numbers, bandwidth_phone_number):
    """
    Main method for the script

    Args:
        phone_numbers (list<string): The phone numbers to use for the conference
        bandwidth_phone_number (str): The Bandwidth phone number to send the ending group text

    Returns:
        void
    """
    conference_id = start_conference(phone_numbers, bandwidth_phone_number)
    end_conference_with_text(conference_id, bandwidth_phone_number)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 5 or len(sys.argv) > 12:
        print("You must have at least 3 phone numbers to make a conference call. The maximum number of phone numbers allowed is 10")
        print(usage)
        exit(-1)

    main(sys.argv[1:-1], sys.argv[-1])

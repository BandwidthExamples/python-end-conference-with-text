<div align="center">

# End A Conference Call With A Group Text Message

<a href="http://dev.bandwidth.com"><img src="https://s3.amazonaws.com/bwdemos/BW_Messaging.png"/></a>
<a href="http://dev.bandwidth.com"><img src="https://s3.amazonaws.com/bwdemos/BW_Voice.png"/></a>
</div>

Ever had a conference call where you wanted to end the conference with a text message recap of the meeting? This project shows how you can do that using Bandwidth's Voice and Messaging APIs!

## Table of Contents

* [Prereqs](#prereqs)
* [How It Works](#how-it-works)

## Prereqs

* Bandwidth Application Account (https://app.bandwidth.com)
* Bandwidth V2 Messaging Account (https://go.bandwidth.com/messaging-v2-api.html)
* A server to run the application, or a tunneling service like ngrok

## How It Works

This project is a simple python script that starts a conference call, and ends the conference call with a group text message.

Before running the project, the following environmental variables need to be set:

```
BANDWIDTH_USER_ID
BANDWIDTH_API_SECRET
BANDWIDTH_API_TOKEN
BANDWIDTH_PHONE_NUMBER
USER_PHONE_NUMBER
```

Phone numbers must be in +1XXXYYYZZZZ format.

The python version used in this project is 3.7.0.

Required dependencies can be installed by running the following command:

```
pip install -r requirements.txt
```

To start the server, run the following command

```
python conference_call.py
```

### Setting up the Bandwidth application
Login to https://app.bandwidth.com and create a Bandwidth Application. This application will be both a voice and messaging application. Assign your BANDWIDTH_PHONE_NUMBER to this application.

Make the `Voice callback URL` point to `<your-server>/voice` and the `Messaging callback URL` point to `<your-server>/message`

### Starting the conference
After the server has started, you can text your BANDWIDTH_PHONE_NUMBER from your USER_PHONE_NUMBER a list of numbers to start a conference.

Example text message:

```
+1XXXYYYZZZZ +1AAABBBCCCC +1DDDEEEFFFF
```

Note that your USER_PHONE_NUMBER needs to also be included if you want to be included in the conference call.

You can send up to 10 numbers.

You will receive a response from your BANDWIDTH_PHONE_NUMBER that looks like this:

```
Your conference has been created. Your requested members of the conference will receive a text message asking them to join the conference.
```

Each of the numbers you requested to join the conference will receive a text message that looks like this:

```
You have been invited by USER_PHONE_NUMBER to join a conference. Please call BANDWIDTH_PHONE_NUMBER to join
```

After calling the BANDWIDTH_PHONE_NUMBER, the member will join the conference

###Ending the conference
The next text message sent by USER_PHONE_NUMBER will signal the end of the conference. You can send anything you like, and that text message will be forwarded to all members of the conference.

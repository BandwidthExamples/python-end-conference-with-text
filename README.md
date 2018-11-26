<div align="center">

# Title

<a href="http://dev.bandwidth.com"><img src="https://s3.amazonaws.com/bwdemos/BW_Messaging.png"/></a>
<a href="http://dev.bandwidth.com"><img src="https://s3.amazonaws.com/bwdemos/BW_Voice.png"/></a>
</div>

Short description of project

## Table of Contents

* [Prereqs](#prereqs)
* [How It Works](#how-it-works)

## Prereqs

* Bandwidth Application Account (https://app.bandwidth.com)
* Bandwidth V2 Messaging Account (https://go.bandwidth.com/messaging-v2-api.html)

## How It Works

This project is a simple python script that starts a conference call, and ends the conference call with a group text message

Before running the project, the following environmental variables need to be set

```
BANDWIDTH_USER_ID
BANDWIDTH_API_SECRET
BANDWIDTH_API_TOKEN
```

To start the project, run the following command

```
python conference_call.py <member-1-number> <member-2-number> ... <member-n-number> <bandwidth_phone_number>
```

Phone numbers must be in +1XXXYYYZZZZ format

There is a limit of 10 member numbers for sending a group text, and you must have at least 3 numbers to make a conference call.
The <bandwidth_phone_number> is your Bandwidth phone number that will start the conference call and send the ending group text.

Example
```
python conference_call.py +19191112222 +19191112223 +19191112224 +18281112222
```

In this example, the 3 conference members will be `+19191112222 +19191112223 +19191112224` and the phone number for starting the conference and senting the final group text will be `+18281112222`

After starting the conference call, you will receive a prompt that looks like this

```
Conference call has been started by +18281112222 to ['+19191112222', '+19191112223', '+19191112224']
Please type your ending text message and press enter when you are ready to end conference conf-34dladc3:

```

Type in your message and press enter to end the conference with the group text

```
Please type your ending text message and press enter when you are ready to end conference conf-34dladc3:
We're done! Please remember to schedule time for our next meeting.
Conference conf-34dladc3 has been ended. Group text send by +18281112222
Group text message: We're done! Please remember to schedule time for our next meeting.
```

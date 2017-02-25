import json
from datetime import datetime, timedelta
from random import randint
from time import sleep

import requests

# Header, which is included with every call. This contains among other tings the device ID (as x-player-token) of
# the Android device, and the user-agent which the app uses.
headers = {'x-player-token': 'android:PASTE-ANDROID-DEVICE-ID-HERE', 'user-agent': 'okhttp/3.4.1',
           'Content-Type': 'application/json;charset=utf-8', 'Connection': 'Keep-Alive'}
# Data, which is used to initiate the connection. This registers the token with the x-player-token. This allows to
# kamergotchi to send push notifications to your device. This might not be needed
data = {'platform': 'android',
        'token': "PASTE-YOUR-PUSH-TOKEN-HERE"}

# Different bodies which are sent to the API when you press a button in the app. This script emulates the button
# presses by sending the request directly
data_attention = {'bar': 'attention'}
data_food = {'bar': 'food'}
data_knowledge = {'bar': 'knowledge'}


def parse_result(result):
    """
    This function "parses" the result (json) which is returned from the kamergotchi api
    :param result:  json; result from http-api
    :return: multiple values
    """
    current_knowledge = int(result['game']['current']['knowledge'])
    current_food = int(result['game']['current']['food'])
    current_attention = int(result['game']['current']['attention'])
    care_left = int(result['game']['careLeft'])
    score = int(result['game']['score'])
    day_score = int(result['game']['dayScore'])
    days_alive = int(result['game']['daysAlive'])
    claim_reset = datetime.strptime(result['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
    care_reset = datetime.strptime(result['game']['careReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
    return current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive


def initialize(session):
    """
    Used to associate the Token with the X-Player-token. This allows Kamergotchi to send push notifications
    :param session: Session
    :return: HTTP statuscode; 200 when OK.
    """
    result = session.post("https://api.kamergotchi.nl/players/register-push", headers=headers, data=json.dumps(data))
    return result.status_code


def get_game(session):
    result = session.get("https://api.kamergotchi.nl/game", headers=headers)
    if result.status_code is 200:
        return parse_result(json.loads(result.content.decode('utf-8')))
    else:
        print("ERROR, get_game ", result.status_code, result.content)


def give_food(session):
    print("Giving food...")
    result = session.post("https://api.kamergotchi.nl/game/care", headers=headers, data=json.dumps(data_food))
    if result.status_code is 200:
        return parse_result(json.loads(result.content.decode('utf-8')))
    else:
        print("ERROR, give_food ", result.status_code, result.content)


def give_attention(session):
    print("Giving attention...")
    result = session.post("https://api.kamergotchi.nl/game/care", headers=headers, data=json.dumps(data_attention))
    if result.status_code is 200:
        return parse_result(json.loads(result.content.decode('utf-8')))
    else:
        print("ERROR, give_attention ", result.status_code, result.content)


def give_knowledge(session):
    print("Giving knowledge...")
    result = session.post("https://api.kamergotchi.nl/game/care", headers=headers, data=json.dumps(data_knowledge))
    if result.status_code is 200:
        return parse_result(json.loads(result.content.decode('utf-8')))
    else:
        print("ERROR, give_knowledge ", result.status_code, result.content)


def claim_bonus(session):
    print("Claiming bonus...")
    result = session.post("https://api.kamergotchi.nl/game/claim", headers=headers)
    if result.status_code is 200:
        return parse_result(json.loads(result.content.decode('utf-8')))
    else:
        print("ERROR, claim_bonus ", result.status_code, result.content)


if __name__ == '__main__':
    with requests.Session() as s:
        print("Initializing Session...")
        # Loop until we get a HTTP 200; The server might also respond with other codes like 403 or 502
        while 1:
            # r = HTTP Status code
            r = initialize(s)
            if r is 200:
                # Break out of loop, while giving a message to the user
                print("Initialized Session!")
                break
        # Update all our values accordingly
        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = get_game(
            s)

        # This is the main loop
        while 1:
            # These prints allow for a nicely formatted 'table' which is printed to the screen.
            # The timedelta's are needed because the time which the server returns isn't UTC+1
            print("======================================================")
            print("Current time:\t\t", datetime.now())
            print("")
            print("Knowledge:\t\t", current_knowledge)
            print("Food:\t\t\t", current_food)
            print("Attention:\t\t", current_attention)
            print("")
            print("Care left:\t\t", care_left)
            print("Care reset:\t\t", care_reset + timedelta(hours=1))
            print("Claim reset:\t\t", claim_reset + timedelta(hours=1))
            print("")
            print("Score:\t\t\t", score)
            print("Score today:\t\t", day_score)
            print("")
            print("Days alive:\t\t", days_alive)
            print("======================================================")

            # This checks if there is a bonus which we can claim. This can probably be removed since we are also
            # checking this when our Kamergotchi is "geschorst"
            if claim_reset + timedelta(hours=1) < datetime.now():
                current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = claim_bonus(
                    s)

            # This is true when we can give food, knowledge or attentions to our kamergotchi. This doesn't work
            # properly because the API also returns 0 when we didn't use any of our 'cares' at all. We workaround
            # this limitation by manually setting care_left to 10 later on
            if care_left > 0:
                while care_left > 0:
                    # This allows for a small randomization. This way it doesn't seem like we're pressing 10 buttons
                    # at once. Making it less obvious that our kamergotchi is automated
                    randint(0, 5)
                    # This is true when Food is the lowest OR food and attention are as high as knowledge
                    if current_food <= current_attention and current_food <= current_knowledge:
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = give_food(
                            s)
                    # This happens when current_attention is the lowest
                    elif current_attention <= current_knowledge:
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = give_attention(
                            s)
                    # This happens when current_knowledge is the lowest
                    else:
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = give_knowledge(
                            s)
            # This happens when our kamergotchi is temporarily "geschorst"
            else:
                # Give a nice status update :D
                print("Sleeping....")
                current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = get_game(
                    s)
                while 1:
                    # This allows for a small randomization. This way we aren't kicking off the claiming of bonuses
                    # and giving care to our kamergotchi right after the 'schorsing' is over.
                    sleep(randint(0, 15))
                    # This is true when we're allowed to give Food, Knowledge or Attention to our kamergotchi again.
                    if care_reset + timedelta(hours=1) < datetime.now():
                        care_left = 10
                        break
                    # This is true when we're allowed to claim our bonus again.
                    elif claim_reset + timedelta(hours=1) < datetime.now():
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset, score, day_score, days_alive = claim_bonus(
                            s)

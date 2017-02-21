import json
from datetime import datetime, timedelta
from time import sleep

import requests

data = {"platform": "android",
        "token": "PASTE-YOUR-TOKEN-HERE"}
headers = {'x-player-token': 'android:ANDROID-DEVICE-ID-HERE', 'user-agent': 'okhttp/3.4.1',
           'Content-Type': 'application/json;charset=utf-8', 'Connection': 'Keep-Alive'}
data_attention = {'bar': 'attention'}
data_food = {'bar': 'food'}
data_knowledge = {'bar': 'knowledge'}


def initialize(s):
    r = s.post("http://api.kamergotchi.nl/players/register-push", headers=headers, data=json.dumps(data))
    return r.status_code


def get_game(s):
    r = s.get("http://api.kamergotchi.nl/game", headers=headers)
    if r.status_code is 200:
        result = json.loads(r.content.decode('utf-8'))
        current_knowledge = int(result['game']['current']['knowledge'])
        current_food = int(result['game']['current']['food'])
        current_attention = int(result['game']['current']['attention'])
        care_left = int(result['game']['careLeft'])
        claim_reset = datetime.strptime(result['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        care_reset = datetime.strptime(result['game']['careReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset
    else:
        print("ERROR, get_game ", r.status_code, r.content)
        quit()


def give_food(s):
    print("Giving food...")
    r = s.post("http://api.kamergotchi.nl/game/care", headers=headers, data=json.dumps(data_food))
    if r.status_code is 200:
        result = json.loads(r.content.decode('utf-8'))
        current_knowledge = int(result['game']['current']['knowledge'])
        current_food = int(result['game']['current']['food'])
        current_attention = int(result['game']['current']['attention'])
        care_left = int(result['game']['careLeft'])
        claim_reset = datetime.strptime(result['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        care_reset = datetime.strptime(result['game']['careReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset
    else:
        print("ERROR, give_food ", r.status_code, r.content)
        quit()


def give_attention(s):
    print("Giving attention...")
    r = s.post("http://api.kamergotchi.nl/game/care", headers=headers, data=json.dumps(data_attention))
    if r.status_code is 200:
        result = json.loads(r.content.decode('utf-8'))
        current_knowledge = int(result['game']['current']['knowledge'])
        current_food = int(result['game']['current']['food'])
        current_attention = int(result['game']['current']['attention'])
        care_left = int(result['game']['careLeft'])
        claim_reset = datetime.strptime(result['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        care_reset = datetime.strptime(result['game']['careReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset
    else:
        print("ERROR, give_attention ", r.status_code, r.content)
        quit()


def give_knowledge(s):
    print("Giving knowledge...")
    r = s.post("http://api.kamergotchi.nl/game/care", headers=headers, data=json.dumps(data_knowledge))
    if r.status_code is 200:
        result = json.loads(r.content.decode('utf-8'))
        current_knowledge = int(result['game']['current']['knowledge'])
        current_food = int(result['game']['current']['food'])
        current_attention = int(result['game']['current']['attention'])
        care_left = int(result['game']['careLeft'])
        claim_reset = datetime.strptime(result['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        care_reset = datetime.strptime(result['game']['careReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset
    else:
        print("ERROR, give_knowledge ", r.status_code, r.content)
        quit()


def claim_bonus(s):
    print("Claiming bonus...")
    r = s.post("http://api.kamergotchi.nl/game/claim", headers=headers)
    if r.status_code is 200:
        result = json.loads(r.content.decode('utf-8'))
        current_knowledge = int(result['game']['current']['knowledge'])
        current_food = int(result['game']['current']['food'])
        current_attention = int(result['game']['current']['attention'])
        care_left = int(result['game']['careLeft'])
        claim_reset = datetime.strptime(result['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        care_reset = datetime.strptime(result['game']['careReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset
    else:
        print("ERROR, claim_bonus ", r.status_code, r.content)
        quit()


if __name__ == '__main__':
    with requests.Session() as s:
        print("Initializing Session...")
        while 1:
            r = initialize(s)
            if r is 200:
                print("Initialized Session!")
                break
        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = get_game(s)

        while 1:
            print("======================================================")
            print("Current time:\t\t", datetime.now())
            print("")
            print("Knowledge:\t\t", current_knowledge)
            print("Food:\t\t\t", current_food)
            print("Attention:\t\t", current_attention)
            print("")
            print("Care left:\t\t", care_left)
            print("Claim reset:\t\t", claim_reset + timedelta(hours=1))
            print("Care reset:\t\t", care_reset + timedelta(hours=1))
            print("======================================================")

            if claim_reset + timedelta(hours=1) < datetime.now():
                current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = claim_bonus(s)
            else:
                print("Can't claim bonus yet")

            if care_left > 0:
                while care_left > 0:
                    if current_food <= current_attention and current_food <= current_knowledge:
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = give_food(
                            s)
                    elif current_attention <= current_knowledge:
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = give_attention(
                            s)
                    else:
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = give_knowledge(
                            s)
            else:
                print("Sleeping....")
                current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = get_game(s)
                while 1:
                    sleep(2)
                    if care_reset + timedelta(hours=1) < datetime.now():
                        care_left = 10
                        break
                    elif claim_reset + timedelta(hours=1) < datetime.now():
                        current_knowledge, current_food, current_attention, care_left, claim_reset, care_reset = claim_bonus(
                            s)

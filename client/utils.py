from random import randrange
import json

import config

def random_squawk(length=4):
    return "".join([str(randrange(0, 8)) for _ in range(length)])

def validate_squawk(squawk):
    if squawk == "":
        return False
    for c in squawk:
        if not c.isdigit():
            return False
        if not (0 <= int(c) < 8):
            return False
    return True

def generate_squawk(service, rule, mainWidget):
    if service == config.conspicuity_service:
        return config.flight_rules[rule]
    
    min = int(config.services[service][0], 8)
    max = int(config.services[service][1], 8)

    used_squawks = []

    for r in mainWidget.sections:
        for section in r:
            for strip in section.strips:
                used_squawks.append(strip.m3)

    for squawk in range(min, max+1):
        if not f"{int(str(oct(squawk))[2:]):04}" in used_squawks:
            return f"{int(str(oct(squawk))[2:]):04}"

def load_data():
    with open("data.json", "r") as f:
        data = json.loads(f.read())

    return data

def load_aerodromes():
    with open("aerodromes.json", "r") as f:
        data = json.loads(f.read())

    return data

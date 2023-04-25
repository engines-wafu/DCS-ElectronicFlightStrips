from random import randrange
import json

def random_squawk(length: int=4) -> str:
    return "".join([str(randrange(0, 8)) for _ in range(length)])

def validate_squawk(squawk: str) -> bool:
    if squawk == "":
        return False
    for c in squawk:
        if not c.isdigit():
            return False
        if not (0 <= int(c) < 8):
            return False
    return True

def generate_squawk(service: str, rule: str, mainWidget) -> str:
    if service == mainWidget.config["conspicuity_service"]:
        return mainWidget.config["flight_rules"][rule]
    
    min = int(mainWidget.config["services"][service][0], 8)
    max = int(mainWidget.config["services"][service][1], 8)

    used_squawks = []

    for r in mainWidget.sections:
        for section in r:
            for strip in section.strips:
                used_squawks.append(strip.m3)

    for squawk in range(min, max+1):
        if not f"{int(str(oct(squawk))[2:]):04}" in used_squawks:
            return f"{int(str(oct(squawk))[2:]):04}"

def load_data() -> dict:
    with open("data.json", "r") as f:
        data = json.loads(f.read())

    return data

def load_aerodromes() -> dict:
    with open("aerodromes.json", "r") as f:
        data = json.loads(f.read())

    return data

def load_config(p: str=None) -> dict:
    with open("config.json", "r") as f:
        data = json.loads(f.read())
    
    if p:
        for profile in data:
            if profile["profile_name"] == p:
                return profile
    else:
        return data

def validate_config(cfg: dict) -> bool:
    for profile in cfg:
        settings = list(profile.keys())
        if not "profile_name" in settings:
            print("profile is unnamed")
            return False
        
        if not "sections" in settings:
            print("no sections defined")
            return False

        if not "inbox" in settings:
            print("no inbox defined")
            return False

        if "column_spans" in settings:
            if max(profile["column_spans"]) > 10:
                print("column_spans invalid")
                return False

        if "flight_rules" in settings:
            for squawk in profile["flight_rules"].values():
                if not validate_squawk(squawk):
                    print("invalid flight rules conspicuity squawk")
                    return False

        if "services" in settings:
            for service in profile["services"]:
                if len(profile["services"][service]) > 2:
                    print("too many squawks in 'services'")
                    return False

                for squawk in profile["services"][service]:
                    if not validate_squawk(squawk):
                        print("invalid service squawk")
                        return False

            if not "conspicuity_service" in settings:
                print("no conspicuity service defined")
                return False

        if "strip_defaults" in settings:
            if not profile["strip_defaults"]["flight_rules"] in list(profile["flight_rules"].keys()):
                print("default flight rules not in flight rules")
                return False

            if not profile["strip_defaults"]["service"] in list(profile["services"].keys()):
                print("default service not in services")
                return False

            if not profile["strip_defaults"]["category"] in list(profile["categories"].keys()):
                print("default category not in categories")
                return False

            if profile["strip_defaults"]["type"] != "":
                data = load_data()
                if not profile["strip_defaults"]["type"] in list(data.keys()):
                    print("invalid default type")
                    return False

            if not validate_squawk(profile["strip_defaults"]["m1"]):
                print("invalid default Mode 1 squawk")
                return False

    return True


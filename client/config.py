sections = [
        ["Inbox", "06R", "06L"],
        ["", "Push", "Departed"]
    ]

column_spans = [10, 4, 5]

inbox = "Inbox"

categories = {
        "Arriving": "#ffc069",
        "Departing": "#69a5ff",
        "Circuit": "lightgreen"
        }

flight_rules = {"VFR": "7001", "IFR": "0000"}
services = {
        "N": ["0000", "0000"],
        "BS": ["0050", "0053"],
        "TS": ["0054", "0057"],
        "DS": ["0060", "0063"],
        "RS": ["0064", "0067"]
        }

conspicuity_service = "N"

defaults = {
        "callsign": "XXX123",
        "flight rules": list(flight_rules.keys())[0],
        "service": list(services.keys())[0],
        "category": list(categories.keys())[0],
        "type": "A20N",
        "fields": "PGUA",
        "m1": "00",
        "hdg": "HXXX",
        "alt": "AXXX",
        "spd": "SXXX"
        }

useEmer = True

emer_squawks = ["7500", "7600", "7700", "0022"]
emer_color = "#f08080"

recat = False

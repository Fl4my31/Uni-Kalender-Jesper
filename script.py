from datetime import datetime
import os
import requests
from icalendar import Calendar, Event

# Dein echter HSW-Abo-Link ist hier bereits eingetragen:
ICS_URL = "https://meinstudium.hsw-elearning.de/Portale/prod/webportale/teilnehmerportal/Member/ShortLink?guid=ca875d64-2f17-4cdd-9b14-b4cf01498292"

def process_calendar():
    print("Lade Uni-Kalender herunter...")
    response = requests.get(ICS_URL)
    response.raise_for_status()
    
    gcal = Calendar.from_ical(response.content)
    days_dict = {}

    for component in gcal.walk():
        if component.name == "VEVENT":
            dtstart = component.get('dtstart')
            dtend = component.get('dtend')
            
            if not dtstart or not dtend:
                continue
                
            start_val = dtstart.dt
            end_val = dtend.dt
            
            # Nur Events mit Uhrzeit berücksichtigen (keine reinen Ganztagesevents)
            if isinstance(start_val, datetime) and isinstance(end_val, datetime):
                day_str = start_val.strftime('%Y-%m-%d')
                
                if day_str not in days_dict:
                    days_dict[day_str] = []
                
                days_dict[day_str].append((start_val, end_val))

    new_cal = Calendar()
    new_cal.add('prodid', '-//Uni Z Zusammenfassungs-Skript//DE')
    new_cal.add('version', '2.0')
    new_cal.add('X-WR-CALNAME', 'Uni-Tage (Familie)')

    for day_str, times in days_dict.items():
        earliest_start = min(t[0] for t in times)
        latest_end = max(t[1] for t in times)
        
        event = Event()
        event.add('summary', 'Uni Jesper')
        event.add('dtstart', earliest_start)
        event.add('dtend', latest_end)
        event.add('description', 'Automatisch zusammengefasster Uni-Tag von der ersten bis zur letzten Veranstaltung.')
        
        new_cal.add_component(event)

    output_path = "familien_uni.ics"
    with open(output_path, "wb") as f:
        f.write(new_cal.to_ical())
    
    print(f"Erfolgreich {len(days_dict)} Tage zusammengefasst und in {output_path} gespeichert.")

if __name__ == "__main__":
    process_calendar()

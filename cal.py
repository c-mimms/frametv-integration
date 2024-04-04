from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime, timedelta, time, timezone
import logging

def extract_datetime_key(event: Event):
    if isinstance(event.start, datetime):
        return event.start
    else:
        return datetime.combine(event.start, time(), tzinfo=timezone.utc)

def get_events_for_next_days(days=3):
    gc = GoogleCalendar(credentials_path='./credentials.json')

    # Get the current date
    now = datetime.now()

    # Calculate the start and end dates
    # Subtract one day from the current date and combine it with a time object representing midnight
    start_date = datetime.combine(now.date(), time())
    end_date = now + timedelta(days=days)

    events_list = []

    for calendar in gc.get_calendar_list():
        if calendar.selected:
            for event in gc.get_events(calendar_id=calendar.calendar_id, single_events=True, time_min=start_date, time_max=end_date):
                logging.info(f'Event: {event} - {event.start}')
                events_list.append(event)

    events_list.sort(key=extract_datetime_key)
    logging.info(f'Returning events list.')

    return events_list
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime, timedelta


def get_events_for_next_days(days=3):
    gc = GoogleCalendar(credentials_path='./credentials.json')

    # Get the current date
    now = datetime.now()

    # Calculate the start and end dates
    start_date = now
    end_date = now + timedelta(days=days)

    events_list = []

    for calendar in gc.get_calendar_list():
        if calendar.selected:
            for event in gc.get_events(calendar_id=calendar.calendar_id, time_min=start_date, time_max=end_date):
                if event.recurrence:
                    # This event is recurring, get the instances within the time period
                    instances = gc.get_instances(event, time_min=start_date, time_max=end_date)
                    events_list.extend(instances)
                else:
                    events_list.append(event)
    
    events_list.sort(key=lambda event: event.start)

    return events_list
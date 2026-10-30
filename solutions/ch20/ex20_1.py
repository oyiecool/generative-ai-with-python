# uv add icalendar
from datetime import date, datetime
from pathlib import Path

from icalendar import Calendar


def todays_events() -> str:
    """List today's events from the local calendar file."""
    path = Path.home() / "calendar.ics"
    if not path.exists():
        return "No calendar file found."
    cal = Calendar.from_ical(path.read_bytes())
    today, items = date.today(), []
    for ev in cal.walk("VEVENT"):
        start = ev.get("dtstart").dt
        d = start.date() if isinstance(start, datetime) else start
        if d == today:
            t = start.strftime("%H:%M") if isinstance(start, datetime) else "all day"
            items.append(f"{t} {ev.get('summary')}")
    return "; ".join(sorted(items)) or "Nothing scheduled today."

TOOLS["todays_events"] = todays_events

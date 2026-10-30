from datetime import datetime


def monitoring_active(now: datetime | None = None) -> bool:
    now = now or datetime.now()
    weekday_hours = now.weekday() < 5 and 8 <= now.hour < 18
    return not weekday_hours

# in the main loop
if diff > CHANGE_THRESHOLD and monitoring_active() and time.time() - last_event > COOLDOWN_S:
    ...

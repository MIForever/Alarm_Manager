import datetime
from alarm_manager import AlarmManager

# Initializing AlarmManager class with "Alarm manager" app title
manager = AlarmManager(app_id="Alarm Manager")

# Only time
# If the time is up. it automatically sets the time for the next day
manager.add_alarm(datetime.time(14, 56), message="This is a reminder.")

# With a date
# Format: Y, M, D, H, M 
manager.add_alarm(datetime.datetime(2023, 9, 26, 15, 30), message="Hurry up to work!")

# Remove an alarm by specifying its time.
alarm_time_to_remove = datetime.time(8, 0) # You can also specify the date (Look above)
manager.remove_alarm(alarm_time_to_remove)

# Get all the alarms
all_alarms = manager.get_all_alarms()
for i in all_alarms:
    print(f"Alarm time: {i.alarm_time}, message: {i.message}")
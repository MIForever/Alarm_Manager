import threading
import pickle
import datetime
import pygame

from winotify import Notification, audio


class Alarm:
    def __init__(self, alarm_time, message):
        self.alarm_time = alarm_time
        self.message = message
        self.thread = None


class AlarmManager:
    def __init__(self, app_id: str, alarm_sound=audio.LoopingAlarm):
        """
        Args:
            app_id: The name appears on the top of the notification
            alarm_sound: audio.Sound class object
        """

        self.__app_id = app_id
        self.alarm_sound = alarm_sound
        self.alarms = []
        self.load_alarms()

    def play_audio(self):
        pygame.mixer.init()

        pygame.mixer.music.load(self.alarm_sound)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def add_alarm(self, alarm_time, message):
        now = datetime.datetime.now()
        alarm_datetime = self.parse_alarm_time(alarm_time, now)

        if alarm_datetime < now:
            alarm_datetime += datetime.timedelta(days=1)

        alarm = Alarm(alarm_datetime, message)
        alarm.thread = threading.Thread(target=self.run_alarm, args=(alarm,))
        alarm.thread.start()

        self.alarms.append(alarm)
        self.save_alarms()

    def remove_alarm(self, alarm_time):
        for alarm in self.alarms:
            if alarm.alarm_time == alarm_time:
                alarm.thread.cancel()
                self.alarms.remove(alarm)
                self.save_alarms()
                break

    def parse_alarm_time(self, alarm_time, current_time):
        if isinstance(alarm_time, datetime.datetime):
            return alarm_time
        elif isinstance(alarm_time, datetime.time):
            return datetime.datetime.combine(current_time.date(), alarm_time)
        else:
            raise ValueError("Invalid alarm_time format")

    def run_alarm(self, alarm):
        time_until_alarm = (alarm.alarm_time - datetime.datetime.now()).total_seconds()
        if time_until_alarm > 0:
            threading.Timer(time_until_alarm, self.trigger_alarm, args=(alarm,)).start()
        else:
            self.trigger_alarm(alarm)

    def trigger_alarm(self, alarm: Alarm):
        toast = Notification(
            app_id=self.__app_id,
            title="Alarm",
            msg=alarm.message,
            duration="long",
        )

        toast.add_actions(label="Stop")
        toast.set_audio(self.alarm_sound, loop=True)
        toast.show()

        self.play_audio()
        print(alarm.message)

    def save_alarms(self):
        serialized_alarms = [
            {"alarm_time": alarm.alarm_time, "message": alarm.message}
            for alarm in self.alarms
        ]
        with open("alarms.pickle", "wb") as f:
            pickle.dump(serialized_alarms, f)

    def load_alarms(self):
        try:
            with open("alarms.pickle", "rb") as f:
                serialized_alarms = pickle.load(f)
                now = datetime.datetime.now()

                for serialized_alarm in serialized_alarms:
                    alarm_time = serialized_alarm["alarm_time"]
                    message = serialized_alarm["message"]

                    if alarm_time > now:
                        self.add_alarm(alarm_time, message)
        except FileNotFoundError:
            self.alarms = []

    def get_all_alarms(self):
        return self.alarms
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import threading
import time
import os
from playsound import playsound
import pygame
import json

sound_directory = 'sound'

# TODO:
#  Add the Alarm sound and logics:

ALARM_SETTINGS_FILE = 'alarm_settings.json'


def save_alarms(alarms):
    with open(ALARM_SETTINGS_FILE, 'w') as f:
        json.dump(alarms, f)


def load_alarms():
    try:
        with open(ALARM_SETTINGS_FILE, 'r') as f:
            alarms = json.load(f)
        return alarms
    except FileNotFoundError:
        return []

def play_alarm_sound(sound_path, volume):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(volume / 100)  # Set the volume
    pygame.mixer.music.play()


def wait_for_alarm(alarm_time, repeat, sound_path):
    while True:
        now = datetime.now()
        if now >= alarm_time:
            play_alarm_sound(sound_path)
            if not repeat:
                break
            alarm_time += timedelta(days=1)
        time.sleep(10)  # Check every 10 seconds


def list_sound_files(sound_directory):
    sound_files = [f for f in os.listdir(sound_directory) if f.endswith(('.mp3', '.wav'))]
    return sound_files


class TimePickerFrame(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self['bg'] = '#343a40'
        self.return_callback = return_callback

        # Header
        self.header_frame = tk.Frame(self, bg='#343a40')
        self.header_frame.pack(fill=tk.X)
        self.title_label = tk.Label(self.header_frame, text="Alarm", font=("Courier New", 16), )
        self.title_label.pack(side=tk.TOP, fill=tk.X)
        self.time_selection_frame = tk.Frame(self, bg=self['bg'])
        self.time_selection_frame.pack(pady=20)

        self.sound_var = tk.StringVar()
        self.sound_selector = ttk.Combobox(self, textvariable=self.sound_var, state="readonly")
        self.sound_selector['values'] = list_sound_files(sound_directory)
        self.sound_selector.set(self.sound_selector['values'][0] if self.sound_selector['values'] else 'No Sound')
        self.sound_selector.bind('<<ComboboxSelected>>', self.play_selected_sound)
        self.volume_scale = tk.Scale(self, from_=0, to=100, orient='horizontal', bg=self['bg'], fg='white',
                                     command=self.adjust_volume)

        self.sound_selector.pack()

        tk.Label(self.time_selection_frame, text="HR:", bg=self['bg'], fg='white').pack(side=tk.LEFT)
        self.hour_cb = ttk.Combobox(self.time_selection_frame, values=[f'{i:02d}' for i in range(24)], width=3,
                                    state="readonly")
        self.hour_cb.pack(side=tk.LEFT)
        tk.Label(self.time_selection_frame, text="MIN:", bg=self['bg'], fg='white').pack(side=tk.LEFT)
        self.minute_cb = ttk.Combobox(self.time_selection_frame, values=[f'{i:02d}' for i in range(60)], width=3,
                                      state="readonly")
        self.minute_cb.pack(side=tk.LEFT)
        tk.Label(self.time_selection_frame, text="SEC:", bg=self['bg'], fg='white').pack(side=tk.LEFT)
        self.second_cb = ttk.Combobox(self.time_selection_frame, values=[f'{i:02d}' for i in range(60)], width=3,
                                      state="readonly")
        self.second_cb.pack(side=tk.LEFT)

        self.hour_cb.set("00")
        self.minute_cb.set("00")
        self.second_cb.set("00")

        # Reapet option
        self.repeat_label = tk.Label(self, text="Repeat", bg=self['bg'], fg='white')
        self.repeat_label.pack()
        self.repeat_var = tk.StringVar()
        self.repeat_cb = ttk.Combobox(self, textvariable=self.repeat_var,
                                      values=["No Repeat", "Everyday", "Weekdays", "Weekends"], state="readonly")
        self.repeat_cb.set("No Repeat")
        self.repeat_cb.pack()

        # Sound Selector
        self.sound_label = tk.Label(self, text="Sound", bg=self['bg'], fg='white')
        self.sound_label.pack()
        self.sound_var = tk.StringVar()
        self.sound_selector = ttk.Combobox(self, textvariable=self.sound_var, state="readonly")
        self.sound_selector['values'] = ['Beep', 'Chime', 'Ringtone']
        self.sound_selector.set('Beep')
        self.sound_selector.pack()

        self.volume_label = tk.Label(self, text="Volume", bg=self['bg'], fg='white')
        self.volume_label.pack()
        self.volume_scale = tk.Scale(self, from_=0, to=100, orient='horizontal', bg=self['bg'], fg='white')
        self.volume_scale.set(50)  # Default volume level
        self.volume_scale.pack()

        self.set_button = tk.Button(self, text="Set", command=self.on_set, bg='white')
        self.set_button.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

        self.back_button = tk.Button(self, text='Back', command=self.on_back, bg='white')
        self.back_button.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)

    def on_back(self):
        self.return_callback(None)

    def adjust_volume(self, volume_level):
        volume = int(volume_level) / 100
        pygame.mixer.music.set_volume(volume)

    def play_selected_sound(self, event=None):
        sound_file = os.path.join(sound_directory, self.sound_selector.get())
        if os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()

    def on_set(self):
        selected_time = (self.hour_cb.get(), self.minute_cb.get(), self.second_cb.get())
        repeat_option = self.repeat_var.get()
        sound_option = self.sound_selector.get()
        volume_level = self.volume_scale.get()
        self.return_callback((selected_time, repeat_option, sound_option, volume_level))

        alarm_time = datetime.now().replace(hour=int(selected_time[0]),
                                            minute=int(selected_time[1]),
                                            second=int(selected_time[2]),
                                            microsecond=0)

        if alarm_time <= datetime.now():
            alarm_time += timedelta(days=1)

        repeat_option = self.repeat_var.get() == 'Everyday'
        sound_option = self.sound_selector.get()
        volume_level = self.volume_scale.get()

        # Start the alarm thread
        alarm_thread = threading.Thread(target=self.wait_for_alarm, args=(alarm_time, repeat_option, sound_option),
                                        daemon=True)
        alarm_thread.start()
        save_alarms(self.alarms)



    def wait_for_alarm(self, alarm_time, repeat, sound_option):
        while True:
            now = datetime.now()
            if now >= alarm_time:
                play_alarm_sound(os.path.join(sound_directory, sound_option))
                if not repeat:
                    break
                alarm_time += timedelta(days=1)
            time.sleep(10)


class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("TickTalker App")
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.alarm_time = None
        self.repeat_alarm = False
        self.alarm_sound_path = "alarm.mp3"

        master.geometry("360x576")  # Width x Height

        # Styling constants
        background_color = "#343a40"
        button_color = "#007bff"
        text_color = "#f8f9fa"
        self.save_alarms = load_alarms()
        self.check_alarms_thread = threading.Thread(target=self.check_alarms, daemon=True)
        self.check_alarms_thread.start()

        master.configure(bg=background_color)

        self.header_label = tk.Label(master, text="TickTalker App", font=("Courier New", 16), bg=background_color,
                                     fg=text_color)
        self.header_label.pack(pady=10)

        self.buttons_frame = tk.Frame(master, bg=background_color)
        self.buttons_frame.pack()

        self.set_timer_button = tk.Button(self.buttons_frame, text="Timer", command=self.set_timer, bg=button_color,
                                          fg=text_color, relief=tk.RAISED)
        self.set_timer_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.set_alarm_button = tk.Button(self.buttons_frame, text="Alarm", command=self.show_alarm_frame,
                                          bg=button_color, fg=text_color, relief=tk.RAISED)
        self.set_alarm_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.set_task_button = tk.Button(self.buttons_frame, text='Task', command=self.set_task, bg=button_color,
                                         fg=text_color, relief=tk.RAISED)
        self.set_task_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.footer_label = tk.Label(master, text="Made with ❤️ by samueladebayo.com", font=("Courier New", 10),
                                     bg=background_color, fg=text_color)
        self.footer_label.pack(side="bottom", pady=5)
        self.alarm_frame = None

    def set_timer(self):
        messagebox.showinfo("Timer", "Timer started!")
        pass

    def show_alarm_frame(self):
        self.header_label.pack_forget()
        self.footer_label.pack_forget()
        self.main_frame.pack_forget()
        self.main_frame.pack_forget()
        if self.alarm_frame is not None:
            self.alarm_frame.destroy()

        self.alarm_frame = TimePickerFrame(self.master, self.return_from_alarm_frame)
        self.alarm_frame.pack(fill=tk.BOTH, expand=True)

    def return_from_alarm_frame(self, selected_time):
        if self.alarm_frame:
            self.alarm_frame.destroy()
        self.alarm_frame = None

        self.header_label.pack(pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.footer_label.pack(side="bottom", pady=5)

    def set_task(self):
        pass

    def check_alarms(self):
        while True:
            now = datetime.now()
            for alarm in self.alarms:
                if now >= alarm['time']:

                    save_alarms(self.alarms)
            time.sleep(60)


if __name__ == "__main__":
    root = tk.Tk()
    my_timer = TimerApp(root)
    root.mainloop()

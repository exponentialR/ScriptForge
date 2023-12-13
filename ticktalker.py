import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import threading
import time
import os
from playsound import playsound


def play_alarm_sound(sound_path):
    if os.path.exists(sound_path):
        playsound(sound_path)
    else:
        messagebox.showerror('Error', 'The sound file does not exist')


def wait_for_alarm(alarm_time, repeat, sound_path):
    while True:
        now = datetime.now()
        if now >= alarm_time:
            play_alarm_sound(sound_path)
            if not repeat:
                break
            alarm_time += timedelta(days=1)
        time.sleep(10)  # Check every 10 seconds


class TimePickerFrame(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.return_callback = return_callback

        self.hours = [f'{i:02d}' for i in range(24)]
        self.minutes = [f'{i:02d}' for i in range(60)]
        self.seconds = [f'{i:02d}' for i in range(60)]

        self.hour_cb = ttk.Combobox(self, values=self.hours, width=3, state="readonly")
        self.minute_cb = ttk.Combobox(self, values=self.minutes, width=3, state="readonly")
        self.second_cb = ttk.Combobox(self, values=self.seconds, width=3, state="readonly")

        self.hour_cb.set("00")
        self.minute_cb.set("00")
        self.second_cb.set("00")

        self.hour_cb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(self, text=":").pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.minute_cb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(self, text=":").pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.second_cb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add set button
        self.set_button = tk.Button(self, text="Set", command=self.on_set)
        self.set_button.pack(side=tk.BOTTOM, pady=10)

    def on_set(self):
        selected_time = (
            self.hour_cb.get(),
            self.minute_cb.get(),
            self.second_cb.get(),
        )
        self.return_callback(selected_time)


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
        self.main_frame.pack_forget()
        if self.alarm_frame:
            self.alarm_frame.destroy()
        self.alarm_frame = TimePickerFrame(self.master, self.return_from_alarm_frame)
        self.alarm_frame.pack(fill=tk.BOTH, expand=True)

    def return_from_alarm_frame(self, selected_time):
        print(f"Selected Time: {selected_time}")

        self.alarm_frame.pack_forget()
        self.alarm_frame = None
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def set_task(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    my_timer = TimerApp(root)
    root.mainloop()
